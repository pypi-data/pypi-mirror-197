#!/usr/bin/python3
# -*- coding: utf-8 -*-

from slpkg.configs import Configs
from slpkg.utilities import Utilities


class FindInstalled(Configs, Utilities):
    """ Find installed packages. """

    def __init__(self):
        super(Configs, self).__init__()
        super(Utilities, self).__init__()
        self.color = self.colour()

        self.yellow: str = self.color['yellow']
        self.cyan: str = self.color['cyan']
        self.green: str = self.color['green']
        self.blue: str = self.color['blue']
        self.endc: str = self.color['endc']
        self.grey: str = self.color['grey']

    def find(self, packages: list, pattern: str) -> None:
        """ Find the packages. """
        matching: list = []

        installed: list = list(self.all_installed(pattern))

        print(f'The list below shows the installed packages '
              f'that contains \'{", ".join([p for p in packages])}\' files:\n')

        for pkg in packages:
            for package in installed:
                if pkg in package:
                    matching.append(package)
        self.matched(matching)

    def matched(self, matching: list) -> None:
        """ Print the matched packages. """
        if matching:
            for package in matching:
                print(f'{self.cyan}{package}{self.endc}')
            print(f'\n{self.grey}Total found {len(matching)} packages.{self.endc}')
        else:
            print('\nDoes not match any package.\n')
