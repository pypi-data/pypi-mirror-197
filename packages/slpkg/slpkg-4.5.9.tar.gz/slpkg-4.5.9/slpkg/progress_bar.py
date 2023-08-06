#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
from progress.spinner import PixelSpinner

from slpkg.configs import Configs


class ProgressBar(Configs):

    def __init__(self):
        super(Configs, self).__init__()
        self.color = self.colour()

        self.bold: str = self.color['bold']
        self.violet: str = self.color['violet']
        self.bviolet: str = f'{self.bold}{self.violet}'
        self.endc: str = self.color['endc']

    def bar(self, message: str, filename: str) -> None:
        """ Creating progress bar. """
        spinner = PixelSpinner(f'{self.endc}{message} {filename} {self.bviolet}')
        # print('\033[F', end='', flush=True)
        while True:
            time.sleep(0.1)
            spinner.next()
