#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import urllib3
from pathlib import Path
from multiprocessing import Process

from slpkg.configs import Configs
from slpkg.progress_bar import ProgressBar


class CheckUpdates(Configs):
    """ Check for changes in the ChangeLog file. """

    def __init__(self):
        super(Configs, self).__init__()
        self.progress = ProgressBar()
        self.color = self.colour()

        self.bold: str = self.color['bold']
        self.green: str = self.color['green']
        self.yellow: str = self.color['yellow']
        self.bgreen: str = f'{self.bold}{self.green}'
        self.endc: str = self.color['endc']

        # Slackbuilds.org repository settings.
        self.changelog_txt: str = self.sbo_chglog_txt
        self.local_chg_txt = Path(self.sbo_repo_path, self.changelog_txt)
        self.repo_chg_txt: str = f'{self.sbo_repo_url}{self.changelog_txt}'

    def check(self) -> bool:
        """ Checks the ChangeLogs and returns True or False. """
        local_date: int = 0

        # Ponce repository settings.
        if self.ponce_repo:
            self.changelog_txt: str = self.ponce_chglog_txt
            self.local_chg_txt = Path(self.ponce_repo_path, self.changelog_txt)
            self.repo_chg_txt: str = f'{self.ponce_repo_url}{self.changelog_txt}'

        http = urllib3.PoolManager()
        repo = http.request('GET', self.repo_chg_txt)

        if self.local_chg_txt.is_file():
            local_date = int(os.stat(self.local_chg_txt).st_size)

        repo_date: int = int(repo.headers['Content-Length'])

        return repo_date != local_date

    def view_message(self) -> None:
        if self.check():
            print(f'\n\n{self.bgreen}There are new updates available!{self.endc}')
        else:
            print(f'\n\n{self.endc}{self.yellow}No updated packages since the last check.{self.endc}')

    def updates(self) -> None:
        """ Starting multiprocessing download process. """
        message: str = f'Checking for news in the {self.changelog_txt} file...'

        # Starting multiprocessing
        p1 = Process(target=self.view_message)
        p2 = Process(target=self.progress.bar, args=(message, ''))

        p1.start()
        p2.start()

        # Wait until process 1 finish
        p1.join()

        # Terminate process 2 if process 1 finished
        if not p1.is_alive():
            p2.terminate()

        # Wait until process 2 finish
        p2.join()

        # Restore the terminal cursor
        print('\x1b[?25h', self.endc)
