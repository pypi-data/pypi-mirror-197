#!/usr/bin/python3
# -*- coding: utf-8 -*-

from typing import Generator

from slpkg.configs import Configs
from slpkg.queries import SBoQueries
from slpkg.utilities import Utilities
from slpkg.blacklist import Blacklist
from slpkg.dependencies import Requires


class Upgrade(Configs, Utilities):
    """ Upgrade the installed packages. """

    def __init__(self, file_pattern):
        super(Configs, self).__init__()
        super(Utilities, self).__init__()
        self.file_pattern: str = file_pattern

        self.black = Blacklist()

    def packages(self) -> Generator[str, None, None]:
        """ Compares version of packages and returns the maximum. """
        upgrade: list = []
        requires: list = []
        repo_packages: list = SBoQueries('').sbos()
        black: list = self.black.packages()

        installed: list = list(self.all_installed(self.file_pattern))

        for pkg in installed:
            inst_pkg_name: str = self.split_installed_pkg(pkg)[0]

            if inst_pkg_name not in black and inst_pkg_name in repo_packages:

                if self.is_package_upgradeable(inst_pkg_name, self.file_pattern):
                    requires += Requires(inst_pkg_name).resolve()
                    upgrade.append(inst_pkg_name)

        # Clean the packages if they are dependencies
        for pkg in upgrade:
            if pkg not in requires:
                yield pkg
