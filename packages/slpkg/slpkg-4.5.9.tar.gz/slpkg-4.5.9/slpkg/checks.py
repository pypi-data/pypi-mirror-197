#!/usr/bin/python3
# -*- coding: utf-8 -*-

from pathlib import Path

from slpkg.configs import Configs
from slpkg.queries import SBoQueries
from slpkg.blacklist import Blacklist
from slpkg.utilities import Utilities


class Check(Configs, Utilities):
    """ Some checks before proceed. """

    def __init__(self):
        super(Configs, self).__init__()
        super(Utilities, self).__init__()

        self.black = Blacklist()
        self.color = self.colour()

        self.bold: str = self.color['bold']
        self.red: str = self.color['red']
        self.cyan: str = self.color['cyan']
        self.endc: str = self.color['endc']
        self.bred: str = f'{self.bold}{self.red}'

        self.repo_path = self.sbo_repo_path
        if self.ponce_repo:
            self.repo_path = self.ponce_repo_path

    def exists(self, slackbuilds: list) -> list:
        """ Checking if the slackbuild exists in the repository. """
        not_packages: list = []

        for sbo in slackbuilds:

            if sbo in self.black.packages():
                slackbuilds.remove(sbo)

            elif not SBoQueries(sbo).slackbuild():
                not_packages.append(sbo)

            else:
                location = SBoQueries(sbo).location()
                if not Path(self.repo_path, location, sbo).is_dir():
                    not_packages.append(sbo)

        if not_packages:
            raise SystemExit(f"\n[{self.bred}Error{self.endc}]: Packages "
                             f"'{self.cyan}{', '.join(not_packages)}{self.endc}' does not exists.\n")

        return slackbuilds

    def unsupported(self, slackbuilds: list) -> None:
        """ Checking for unsupported slackbuilds. """
        for sbo in slackbuilds:
            sources = SBoQueries(sbo).sources()

            if 'UNSUPPORTED' in sources:
                raise SystemExit(f"\n[{self.bred}Error{self.endc}]: Package "
                                 f"'{self.cyan}{sbo}{self.endc}' unsupported by arch.\n")

    def installed(self, slackbuilds: list, file_pattern: str) -> list:
        """ Checking for installed packages. """
        found, not_found = [], []

        for sbo in slackbuilds:
            package: str = self.is_package_installed(sbo, file_pattern)
            if package:
                pkg: str = self.split_installed_pkg(package)[0]
                found.append(pkg)
            else:
                not_found.append(sbo)

        if not_found:
            raise SystemExit(f'\n[{self.bred}Error{self.endc}]: Not found \'{", ".join(not_found)}\' '
                             'installed packages.\n')

        return found

    def blacklist(self, slackbuilds: list) -> None:
        """ Checking if the packages are blacklisted. """
        packages: list = []

        for package in self.black.packages():
            if package in slackbuilds:
                packages.append(package)

        if packages:
            raise SystemExit(
                f"\nThe packages '{self.cyan}{', '.join(packages)}{self.endc}' is blacklisted.\n"
                f"Please edit the blacklist.toml file in "
                f"{self.etc_path} folder.\n")

    def database(self) -> None:
        """ Checking for empty table """
        db = Path(self.db_path, self.database_name)
        if not SBoQueries('').sbos() or not db.is_file():
            raise SystemExit('\nYou need to update the package lists first.\n'
                             "Please run 'slpkg update'.\n")
