#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re
import time
import shutil
from pathlib import Path
from typing import Generator, Any, Union
from distutils.version import LooseVersion
# from packaging.version import Version

from slpkg.configs import Configs
from slpkg.queries import SBoQueries
from slpkg.blacklist import Blacklist


class Utilities:

    def __init__(self):
        self.configs = Configs
        self.colors = self.configs.colour
        self.color = self.colors()
        self.black = Blacklist()

        self.yellow: str = self.color['yellow']
        self.cyan: str = self.color['cyan']
        self.endc: str = self.color['endc']

    def is_package_installed(self, name: str, pattern: str) -> str:
        """ Returns the installed package name. """
        installed: list = list(self.all_installed(pattern))

        for package in installed:
            pkg: str = self.split_installed_pkg(package)[0]

            if pkg == name:
                return package

        return ''

    def all_installed(self, pattern: str) -> Generator:
        """ Return all installed packages from /val/log/packages folder. """
        var_log_packages = Path(self.configs.log_packages)

        for file in var_log_packages.glob(pattern):
            package_name = self.split_installed_pkg(file.name)[0]

            if package_name not in self.black.packages():
                yield file.name

    def all_installed_names(self, pattern: str) -> Generator:
        """ Return all installed packages names from /val/log/packages folder. """
        var_log_packages = Path(self.configs.log_packages)

        for file in var_log_packages.glob(pattern):
            package_name = self.split_installed_pkg(file.name)[0]

            if package_name not in self.black.packages():
                yield self.split_installed_pkg(file.name)[0]

    @staticmethod
    def remove_file_if_exists(path: str, file: str) -> None:
        """ Clean the old files. """
        archive = Path(path, file)
        if archive.is_file():
            archive.unlink()

    @staticmethod
    def remove_folder_if_exists(path: str, folder: str) -> None:
        """ Clean the old folders. """
        directory = Path(path, folder)
        if directory.exists():
            shutil.rmtree(directory)

    @staticmethod
    def create_folder(path: str, folder: str) -> None:
        """ Creates folder. """
        directory = Path(path, folder)
        if not directory.exists():
            directory.mkdir(parents=True, exist_ok=True)

    def split_installed_pkg(self, package: str) -> list:
        """ Split the package by the name, version, arch, build and tag. """
        name: str = '-'.join(package.split('-')[:-3])
        version: str = ''.join(package[len(name):].split('-')[:-2])
        arch: str = ''.join(package[len(name + version) + 2:].split('-')[:-1])
        build: str = ''.join(package[len(name + version + arch) + 3:].split('-')).replace(self.configs.repo_tag, '')
        tag: str = ''.join(package[len(name + version + arch + build) + 4:].split('-'))

        return [name, version, arch, build, tag]

    def finished_time(self, elapsed_time: float) -> None:
        """ Printing the elapsed time. """
        print(f'\n{self.yellow}Finished Successfully:{self.endc}',
              time.strftime(f'[{self.cyan}%H:%M:%S{self.endc}]',
                            time.gmtime(elapsed_time)))

    def is_package_upgradeable(self, package: str, file_pattern: str) -> Any:
        """ Checks if the package is installed and if it is upgradeable, returns true. """
        installed_version: str = '0'
        installed = self.is_package_installed(package, file_pattern)
        repository_version = str(SBoQueries(package).version())

        repo_build_tag: str = self.read_build_tag(package)
        if not repo_build_tag:
            repo_build_tag: str = ''

        inst_build_tag: str = self.split_installed_pkg(installed)[3]
        if not inst_build_tag:
            inst_build_tag: str = ''

        if not repository_version:
            repository_version: str = '0'

        if installed:
            installed_version: str = self.split_installed_pkg(installed)[1]

        return (str(LooseVersion(repository_version + repo_build_tag)) >
                str(LooseVersion(installed_version + inst_build_tag)))

    def read_build_tag(self, sbo: str) -> str:
        """ Patching SBo TAG from the configuration file. """
        location: str = SBoQueries(sbo).location()
        sbo_script = Path(self.configs.sbo_repo_path, location, sbo, f'{sbo}.SlackBuild')

        if sbo_script.is_file():
            with open(sbo_script, 'r', encoding='utf-8') as f:
                lines = f.readlines()

                for line in lines:
                    if line.startswith('BUILD=$'):
                        return ''.join(re.findall(r'\d+', line))

    @staticmethod
    def is_option(flag: list, flags: list) -> Any:
        """ Checking for flags. """
        return [f for f in flag if f in flags]

    @staticmethod
    def read_packages_from_file(file: Path) -> Generator:
        """ Reads packages from file and split these to list. """
        try:

            with open(file, 'r', encoding='utf-8') as pkgs:
                packages: list = pkgs.read().splitlines()

            for package in packages:
                if package and not package.startswith('#'):
                    if '#' in package:
                        package = package.split('#')[0].strip()

                    yield package

        except FileNotFoundError as err:
            raise SystemExit(f'Error: {err}')

    @staticmethod
    def read_file(file: Union[str, Path]) -> list:
        """ Reads the text file. """
        with open(file, 'r', encoding='utf-8') as f:
            return f.readlines()
