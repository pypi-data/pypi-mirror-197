"""This file is part of OpenSesame.

OpenSesame is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

OpenSesame is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with OpenSesame.  If not, see <http://www.gnu.org/licenses/>.
"""
from libopensesame.py3compat import *
from libopensesame.oslogging import oslogger
from libqtopensesame.extensions import BaseExtension
from libqtopensesame.misc.translate import translation_context
_ = translation_context('updater', category='extension')
import opensesame_extensions
from collections import namedtuple
import opensesame_plugins
import pkgutil
import multiprocessing
import subprocess
import json
import requests
import json
from qtpy.QtCore import QTimer
try:
    from packaging.version import parse
except ImportError:
    from pip._vendor.packaging.version import parse


UpdateInfo = namedtuple('UpdateInfo', ['pkg', 'current', 'latest', 'pypi'])


def _pkg_info(pkg):
    """Retrieves package info through conda. This includes packages that were
    installed through pip.
    
    Parameters
    ----------
    pkg: str
    
    Returns
    -------
    dict
        Package information with several keys, including version and platform
    """
    cmd = ['conda', 'list', pkg, '--full-name', '--json']
    result = subprocess.run(cmd, capture_output=True)
    info = json.loads(result.stdout)
    if len(info) != 1:
        print(f'failed to parse {info}')
        return None, None
    return info[0], parse(info[0]['version'])


def _check_conda(pkg):
    """Checks the latest version of a package on conda"""
    cmd = ['conda', 'search', pkg, '--info', '--json']
    result = subprocess.run(cmd, capture_output=True)
    info = json.loads(result.stdout)
    version = parse('0')
    if pkg not in info:
        return version
    for release in info[pkg]:
        ver = parse(release['version'])
        if not ver.is_prerelease:
            version = max(version, ver)
    return version


def _check_pypi(pkg):
    """Checks the latest version of a package on pypi"""
    req = requests.get(f'https://pypi.python.org/pypi/{pkg}/json')
    version = parse('0')
    if req.status_code == requests.codes.ok:
        j = json.loads(req.text.encode(req.encoding))
        releases = j.get('releases', [])
        for release in releases:
            ver = parse(release)
            if not ver.is_prerelease:
                version = max(version, ver)
    return version


def _check_update(pkg):
    """Checks whether a package can be updated. Returns a UpdateInfo object
    if yes, and None otherwise.
    """
    info, current = _pkg_info(pkg)
    if info is None:
        return
    pypi = info['platform'] == 'pypi'
    latest = _check_pypi(pkg) if pypi else _check_conda(pkg)
    if latest <= current:
        return
    return UpdateInfo(pkg, current, latest, pypi)


def _check_updates(queue, pkgs):
    """The main process function that checks for each package in pkgs whether
    it can be updated, and puts UpdateInfo objects into the queue.
    """"
    available_updates = []
    for pkg in pkgs:
        info = _check_update(pkg)
        if info is not None:
            queue.put(info)
    queue.put(None)


class Updater(BaseExtension):
    
    def __init__(self, main_window, info=None):
        self._widget = None
        self._updates = []
        self._update_script = '# No updates available'
        super().__init__(main_window, info)
    
    def _start_update_process(self):
        pkgs = []
        for pkg in self.unloaded_extension_manager.sub_packages + \
                self.plugin_manager.sub_packages:
            if 'packages' not in pkg.__dict__:
                continue
            if isinstance(pkg.packages, str):
                pkgs.append(pkg.packages)
            elif isinstance(pkg.packages, list):
                pkgs += pkg.packages
        if not pkgs:
            oslogger.debug('no packages to check')
            return
        oslogger.debug('update process started')
        self._queue = multiprocessing.Queue()
        self._update_process = multiprocessing.Process(
            target=_check_updates, args=(self._queue, pkgs))
        self._update_process.start()
        self.extension_manager.fire(
            'register_subprocess', 
            pid=self._update_process.pid,
            description='update_process')
        oslogger.debug('update process started')
        QTimer.singleShot(5000, self._check_update_process)
        
    def _check_update_process(self):
        oslogger.debug('checking update process')
        if self._queue.empty():
            try:
                print('update process still running')
            except ValueError:
                # Is raised when getting the pid of a closed process
                return
            QTimer.singleShot(5000, self._check_update_process)
            return
        info = self._queue.get()
        if info is None:
            self._finish_update_process()
            return
        self._updates.append(info)
        QTimer.singleShot(10, self._check_update_process)
        
    def _finish_update_process(self):
        self._update_process.join()
        self._update_process.close()
        oslogger.debug('update process closed')
        if not self._updates:
            oslogger.debug('no updates available')
            return
        script = []
        pypi_updates = [info for info in self._updates if info.pypi]
        conda_updates = [info for info in self._updates if not info.pypi]
        if conda_updates:
            script.append(
                '# The following packages can be updated through conda:')
            for info in conda_updates:
                script.append(
                    f'# - {info.pkg} from {info.current} to {info.latest}')
            pkgs = ' '.join([info.pkg for info in pypi_updates])
            script.append(f'%conda update {pkgs} -y')
        if pypi_updates:
            script.append(
                '# The following packages can be updated through pip:')
            for info in pypi_updates:
                script.append(
                    f'# - {info.pkg} from {info.current} to {info.latest}')
            pkgs = ' '.join([info.pkg for info in pypi_updates])
            script.append(f'%pip install {pkgs} --upgrade --no-deps')
        self._update_script = '\n'.join(script)
        self.extension_manager.fire('notify',
                                    message=_('Some packages can be updated'))
        self.create_action()
        
    def create_action(self):
        if self._widget is None and self._updates:
            super().create_action()

    def _show_updates(self):
        if self._widget is None:
            from .update_widget import UpdateWidget
            self._widget = UpdateWidget(self.main_window)
        self.tabwidget.add(self._widget, 'system-software-update',
                           _('Updates available'), switch=True)
        self._widget.set_script(self._update_script)

    def activate(self):
        self._show_updates()

    @BaseExtension.as_thread(5000)
    def event_startup(self):
        self._start_update_process()
