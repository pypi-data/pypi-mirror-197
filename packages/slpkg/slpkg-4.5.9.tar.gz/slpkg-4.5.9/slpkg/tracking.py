#!/usr/bin/python3
# -*- coding: utf-8 -*-

from slpkg.configs import Configs
from slpkg.views.ascii import Ascii
from slpkg.queries import SBoQueries
from slpkg.utilities import Utilities
from slpkg.dependencies import Requires


class Tracking(Configs, Utilities):
    """ Tracking of the package dependencies. """

    def __init__(self, flags: list):
        super(Configs, self).__init__()
        super(Utilities, self).__init__()
        self.flags: list = flags

        self.ascii = Ascii()
        self.color = self.colour()

        self.llc: str = self.ascii.lower_left_corner
        self.hl: str = self.ascii.horizontal_line
        self.vl: str = self.ascii.vertical_line
        self.cyan: str = self.color['cyan']
        self.grey: str = self.color['grey']
        self.yellow: str = self.color['yellow']
        self.endc: str = self.color['endc']
        self.flag_pkg_version: list = ['-p', '--pkg-version']

    def packages(self, packages: list) -> None:
        """ Prints the packages dependencies. """
        print(f"The list below shows the packages with dependencies:\n")

        char: str = f' {self.llc}{self.hl}'
        sp: str = ' ' * 4
        for package in packages:
            pkg = f'{self.yellow}{package}{self.endc}'

            if self.is_option(self.flag_pkg_version, self.flags):
                pkg = f'{self.yellow}{package}-{SBoQueries(package).version()}{self.endc}'

            requires: list = Requires(package).resolve()
            how_many: int = len(requires)

            if not requires:
                requires = ['No dependencies']

            print(pkg)
            print(char, end='')
            for i, req in enumerate(requires, start=1):
                require: str = f'{self.cyan}{req}{self.endc}'

                if self.is_option(self.flag_pkg_version, self.flags):
                    require: str = f'{self.cyan}{req}{self.endc}-{self.yellow}{SBoQueries(req).version()}{self.endc}'

                if i == 1:
                    print(f' {require}')
                else:
                    print(f'{sp}{require}')

            print(f'\n{self.grey}{how_many} dependencies for {package}{self.endc}\n')
