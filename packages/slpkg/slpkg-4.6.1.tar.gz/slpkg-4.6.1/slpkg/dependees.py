#!/usr/bin/python3
# -*- coding: utf-8 -*-

from typing import Generator
from slpkg.configs import Configs
from slpkg.views.ascii import Ascii
from slpkg.queries import SBoQueries
from slpkg.utilities import Utilities
from slpkg.models.models import session as Session
from slpkg.models.models import SBoTable, PonceTable


class Dependees(Configs, Utilities):
    """ Show which packages depend. """

    def __init__(self, packages: list, flags: list):
        super(Configs, self).__init__()
        super(Utilities, self).__init__()
        self.packages: list = packages
        self.flags: list = flags

        self.session = Session
        self.ascii = Ascii()
        self.color = self.colour()

        self.llc: str = self.ascii.lower_left_corner
        self.hl: str = self.ascii.horizontal_line
        self.var: str = self.ascii.vertical_and_right
        self.bold: str = self.color['bold']
        self.violet: str = self.color['violet']
        self.cyan: str = self.color['cyan']
        self.grey: str = self.color['grey']
        self.yellow: str = self.color['yellow']
        self.byellow: str = f'{self.bold}{self.yellow}'
        self.endc: str = self.color['endc']
        self.flag_full_reverse: list = ['-E', '--full-reverse']
        self.flag_pkg_version: list = ['-p', '--pkg-version']

        # Switch between sbo and ponce repository.
        self.sbo_table = SBoTable
        if self.ponce_repo:
            self.sbo_table = PonceTable

    def slackbuilds(self):
        """ Collecting the dependees. """
        print(f"The list below shows the "
              f"packages that dependees on '{', '.join([p for p in self.packages])}':\n")

        for pkg in self.packages:
            dependees: list = list(self.find_requires(pkg))

            package: str = f'{self.byellow}{pkg}{self.endc}'

            if self.is_option(self.flag_pkg_version, self.flags):
                package: str = f'{self.byellow}{pkg}-{SBoQueries(pkg).version()}{self.endc}'

            print(package)

            print(f' {self.llc}{self.hl}', end='')

            if not dependees:
                print(f'{self.cyan} No dependees{self.endc}')

            sp: str = ' ' * 4
            for i, dep in enumerate(dependees, start=1):
                dependency: str = f'{self.cyan}{dep[0]}{self.endc}'

                if self.is_option(self.flag_pkg_version, self.flags):
                    dependency: str = (f'{self.cyan}{dep[0]}{self.endc}-{self.yellow}'
                                       f'{SBoQueries(dep[0]).version()}{self.endc}')

                if i == 1:
                    print(f' {dependency}')
                else:
                    print(f'{sp}{dependency}')

                if self.is_option(self.flag_full_reverse, self.flags):
                    if i == len(dependees):
                        print(" " * 4 + f' {self.llc}{self.hl} {self.violet}{dep[1]}{self.endc}')
                    else:
                        print(" " * 4 + f' {self.var}{self.hl} {self.violet}{dep[1]}{self.endc}')

            print(f'\n{self.grey}{len(dependees)} dependees for {pkg}{self.endc}\n')

    def find_requires(self, sbo: str) -> Generator[str, None, None]:
        """ Find requires that slackbuild dependees. """
        requires: list = self.session.query(self.sbo_table.name, self.sbo_table.requires).all()  # type: ignore
        for req in requires:
            if [r for r in req[1].split() if r == sbo]:
                yield req
