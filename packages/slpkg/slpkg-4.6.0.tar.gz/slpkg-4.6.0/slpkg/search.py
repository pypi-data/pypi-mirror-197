#!/usr/bin/python3
# -*- coding: utf-8 -*-

from slpkg.configs import Configs
from slpkg.queries import SBoQueries


class SearchPackage(Configs):
    """ Search slackbuilds from the repository. """

    def __init__(self):
        super(Configs, self).__init__()
        self.color = self.colour()

        self.yellow: str = self.color['yellow']
        self.cyan: str = self.color['cyan']
        self.endc: str = self.color['endc']
        self.green: str = self.color['green']
        self.grey: str = self.color['grey']

    def package(self, packages: list) -> None:
        """ Searching and print the matched slackbuilds. """
        matching: int = 0

        names: list = SBoQueries('').sbos()

        print(f'The list below shows the repo '
              f'packages that contains \'{", ".join([p for p in packages])}\':\n')

        for name in names:
            for package in packages:
                if package in name:
                    matching += 1
                    desc: str = SBoQueries(name).description().replace(name, '')
                    print(f'{self.cyan}{name}{self.endc}-{self.yellow}{SBoQueries(name).version()}{self.endc}'
                          f'{self.green}{desc}{self.endc}')

        if not matching:
            print('\nDoes not match any package.\n')
        else:
            print(f'\n{self.grey}Total found {matching} packages.{self.endc}')
