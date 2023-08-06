#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
from typing import Any

from slpkg.configs import Configs
from slpkg.views.ascii import Ascii
from slpkg.queries import SBoQueries
from slpkg.utilities import Utilities
from slpkg.blacklist import Blacklist
from slpkg.dialog_box import DialogBox
from slpkg.models.models import LogsDependencies
from slpkg.models.models import session as Session


class ViewMessage(Configs):
    """ Print some messages before. """

    def __init__(self, flags: list):
        super(Configs, self).__init__()
        self.flags: list = flags

        self.session = Session
        self.utils = Utilities()
        self.black = Blacklist()
        self.dialogbox = DialogBox()
        self.ascii = Ascii()
        self.color = self.colour()

        self.yellow: str = self.color['yellow']
        self.cyan: str = self.color['cyan']
        self.red: str = self.color['red']
        self.grey: str = self.color['grey']
        self.violet: str = self.color['violet']
        self.endc: str = self.color['endc']
        self.download_only = self.tmp_slpkg
        self.installed_packages: list = []
        self.flag_resolve_off: list = ['-o', '--resolve-off']
        self.flag_reinstall: list = ['-r', '--reinstall']
        self.flag_yes: list = ['-y', '--yes']
        self.file_pattern: str = f'*{self.repo_tag}'
        self.all_installed: list = list(self.utils.all_installed_names(self.file_pattern))

    def view_packages(self, package, version, mode):
        """ Printing the main packages. """
        color: str = self.red

        if mode in ['install', 'download']:
            color: str = self.cyan
        if mode == 'build':
            color: str = self.yellow
        if mode == 'upgrade':
            color: str = self.violet

        if package in self.all_installed and mode == 'install':
            color = self.grey

        self.ascii.draw_view_package(package, version, color)

    def view_skipping_packages(self, sbo: str, version: str) -> None:
        """ Print the skipping packages. """
        print(f'[{self.yellow}Skipping{self.endc}] {sbo}-{version} {self.red}(already installed){self.endc}')

    def build_packages(self, slackbuilds: list, dependencies: list) -> None:
        """ View packages for build only. """
        self.ascii.draw_package_title_box('The following packages will be build:', 'Build Packages')

        for sbo in slackbuilds:
            version: str = SBoQueries(sbo).version()
            self.view_packages(sbo, version, mode='build')

        if dependencies:
            self.ascii.draw_middle_line()
            self.ascii.draw_dependency_line()

            for sbo in dependencies:
                version: str = SBoQueries(sbo).version()
                self.view_packages(sbo, version, mode='build')

        self.summary(slackbuilds, dependencies, option='build')

    def install_packages(self, slackbuilds: list, dependencies: list, mode: str) -> None:
        """ View packages for install. """
        title: str = 'Install Packages'
        if mode == 'upgrade':
            title: str = 'Upgrade Packages'

        self.ascii.draw_package_title_box('The following packages will be installed or upgraded:', title)

        for sbo in slackbuilds:
            version: str = SBoQueries(sbo).version()
            self.view_packages(sbo, version, mode=mode)

        if dependencies:
            self.ascii.draw_middle_line()
            self.ascii.draw_dependency_line()

            for sbo in dependencies:
                version: str = SBoQueries(sbo).version()
                self.view_packages(sbo, version, mode=mode)

        self.summary(slackbuilds, dependencies, option=mode)

    def download_packages(self, slackbuilds: list, directory: str) -> None:
        """ View downloaded packages. """
        self.ascii.draw_package_title_box('The following packages will be downloaded:', 'Download Packages')

        if directory:
            self.download_only: str = directory

        for sbo in slackbuilds:
            version: str = SBoQueries(sbo).version()
            self.view_packages(sbo, version, mode='download')

        self.summary(slackbuilds, dependencies=[], option='download')

    def remove_packages(self, packages: list, file_pattern: str) -> Any:
        """ View remove packages. """
        if file_pattern:
            self.file_pattern: str = file_pattern

        slackbuilds, dependencies = [], []
        for pkg in packages:
            slackbuilds.append(pkg)

            requires = self.session.query(
                LogsDependencies.requires).filter(  # type: ignore
                    LogsDependencies.name == pkg).first()

            if requires:
                dependencies += requires[0].split()

        if dependencies and not self.utils.is_option(self.flag_resolve_off, self.flags):
            dependencies: list = self.choose_dependencies_for_remove(list(set(dependencies)))

        self.ascii.draw_package_title_box('The following packages will be removed:', 'Remove Packages')

        for pkg in slackbuilds:
            if pkg not in dependencies:
                self._view_removed(pkg)

        if dependencies and not self.utils.is_option(self.flag_resolve_off, self.flags):
            self.ascii.draw_middle_line()
            self.ascii.draw_dependency_line()

            for pkg in dependencies:
                self._view_removed(pkg)
        else:
            dependencies: list = []

        self.summary(slackbuilds, dependencies, option='remove')

        return self.installed_packages, dependencies

    def _view_removed(self, name: str) -> None:
        """ View and creates list with packages for remove. """
        installed = self.utils.all_installed(self.file_pattern)

        if self.utils.is_package_installed(name, self.file_pattern):
            for package in installed:
                pkg: str = self.utils.split_installed_pkg(package)[0]
                if pkg == name:
                    self.installed_packages.append(package)
                    version = self.utils.split_installed_pkg(package)[1]
                    self.view_packages(pkg, version, mode='remove')

    def choose_dependencies_for_remove(self, dependencies: list) -> list:
        """ Choose packages for remove using the dialog box. """
        height: int = 10
        width: int = 70
        list_height: int = 0
        choices: list = []
        title: str = " Choose dependencies you want to remove "

        for package in dependencies:
            repo_ver: str = SBoQueries(package).version()
            inst_pkg: str = self.utils.is_package_installed(package, self.file_pattern)
            choices += [(package, repo_ver, True, f'Package: {inst_pkg}')]

        text: str = f'There are {len(choices)} dependencies:'

        code, tags = self.dialogbox.checklist(text, dependencies, title, height,
                                              width, list_height, choices)

        if not code:
            return dependencies

        os.system('clear')
        return tags

    def summary(self, slackbuilds: list, dependencies: list, option: str) -> None:
        """ View the status of the packages action. """
        slackbuilds.extend(dependencies)
        install = upgrade = remove = 0

        for sbo in slackbuilds:
            installed: str = self.utils.is_package_installed(sbo, self.file_pattern)

            if not installed:
                install += 1
            elif installed and self.utils.is_option(self.flag_reinstall, self.flags):
                upgrade += 1
            elif (installed and self.utils.is_package_upgradeable(sbo, self.file_pattern) and
                  self.utils.is_option(self.flag_reinstall, self.flags)):
                upgrade += 1
            elif installed and option == 'remove':
                remove += 1

        self.ascii.draw_bottom_line()

        if option in ['install', 'upgrade']:
            print(f'{self.grey}Total {install} packages will be '
                  f'installed and {upgrade} will be upgraded.{self.endc}')

        elif option == 'build':
            print(f'{self.grey}Total {len(slackbuilds)} packages '
                  f'will be build in {self.tmp_path} folder.{self.endc}')

        elif option == 'remove':
            print(f'{self.grey}Total {remove} packages '
                  f'will be removed.{self.endc}')

        elif option == 'download':
            print(f'{self.grey}{len(slackbuilds)} packages '
                  f'will be downloaded in {self.download_only} folder.{self.endc}')

    def logs_packages(self, dependencies: list) -> None:
        """ View the logging packages. """
        print('The following logs will be removed:\n')

        for dep in dependencies:
            print(f'{self.yellow}{dep[0]}{self.endc}')
            self.ascii.draw_log_package(dep[1])

        print('Note: After cleaning you should remove them one by one.')

    def question(self) -> None:
        """ Manage to proceed. """
        if not self.utils.is_option(self.flag_yes, self.flags) and self.ask_question:
            answer: str = input('\nDo you want to continue? [y/N] ')
            if answer not in ['Y', 'y']:
                raise SystemExit()
        print()
