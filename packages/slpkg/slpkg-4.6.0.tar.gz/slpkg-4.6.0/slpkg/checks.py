#!/usr/bin/python3
# -*- coding: utf-8 -*-

from pathlib import Path

from slpkg.configs import Configs
from slpkg.queries import SBoQueries
from slpkg.blacklist import Blacklist
from slpkg.utilities import Utilities


class Check(Configs):
    """ Some checks before proceed. """

    def __init__(self):
        super(Configs, self).__init__()
        self.black = Blacklist()
        self.utils = Utilities()
        self.color = self.colour()

        self.bold: str = self.color['bold']
        self.red: str = self.color['red']
        self.cyan: str = self.color['cyan']
        self.endc: str = self.color['endc']
        self.bred: str = f'{self.bold}{self.red}'

        self.repo_path = self.sbo_repo_path
        if self.ponce_repo:
            self.repo_path = self.ponce_repo_path

    def exists_in_the_database(self, slackbuilds: list) -> None:
        """ Checking if the slackbuild exists in the database. """
        not_packages: list = []

        for sbo in slackbuilds:

            if not SBoQueries(sbo).slackbuild():
                not_packages.append(sbo)

            else:
                location = SBoQueries(sbo).location()
                if not Path(self.repo_path, location, sbo).is_dir():
                    not_packages.append(sbo)

        if not_packages:
            raise SystemExit(f"\n[{self.bred}Error{self.endc}]: Packages "
                             f"'{self.cyan}{', '.join(not_packages)}{self.endc}' does not exists.\n")

    def is_package_unsupported(self, slackbuilds: list) -> None:
        """ Checking for unsupported slackbuilds. """
        for sbo in slackbuilds:
            sources = SBoQueries(sbo).sources()

            if 'UNSUPPORTED' in sources:
                raise SystemExit(f"\n[{self.bred}Error{self.endc}]: Package "
                                 f"'{self.cyan}{sbo}{self.endc}' unsupported by arch.\n")

    def is_installed(self, slackbuilds: list, file_pattern: str) -> None:
        """ Checking for installed packages. """
        not_found = []

        for sbo in slackbuilds:
            package: str = self.utils.is_package_installed(sbo, file_pattern)
            if not package:
                not_found.append(sbo)

        if not_found:
            raise SystemExit(f'\n[{self.bred}Error{self.endc}]: Not found \'{", ".join(not_found)}\' '
                             'installed packages.\n')

    def is_blacklist(self, slackbuilds: list) -> None:
        """ Checking if the packages are blacklisted. """
        blacklist: list = []

        for sbo in slackbuilds:
            if sbo in self.black.packages():
                blacklist.append(sbo)

        if blacklist:
            raise SystemExit(
                f"\nThe packages '{self.cyan}{', '.join(blacklist)}{self.endc}' is blacklisted.\n"
                f"Please edit the '{self.black.blacklist_file_toml}' file.\n")

    def is_empty_database(self) -> None:
        """ Checking for empty table """
        db = Path(self.db_path, self.database_name)
        if not SBoQueries('').sbos() or not db.is_file():
            raise SystemExit('\nYou need to update the package lists first.\n'
                             "Please run 'slpkg update'.\n")
