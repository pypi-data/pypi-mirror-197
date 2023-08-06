#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import subprocess
from pathlib import Path
from multiprocessing import Process, Queue

from slpkg.configs import Configs
from slpkg.utilities import Utilities
from slpkg.install_data import CreateData
from slpkg.views.views import ViewMessage
from slpkg.progress_bar import ProgressBar
from slpkg.check_updates import CheckUpdates
from slpkg.models.models import session as Session
from slpkg.models.models import (Base, engine, SBoTable,
                                 PonceTable)


class UpdateRepository(Configs, Utilities):
    """ Deletes and install the data. """

    def __init__(self, flags: list):
        super(Configs, self).__init__()
        super(Utilities, self).__init__()

        self.flags: list = flags
        self.session = Session
        self.view = ViewMessage(self.flags)

        self.progress = ProgressBar()
        self.color = self.colour()

        self.update: int = 0
        self.bold: str = self.color['bold']
        self.green: str = self.color['green']
        self.yellow: str = self.color['yellow']
        self.bgreen: str = f'{self.bold}{self.green}'
        self.endc: str = self.color['endc']
        self.flag_generate: list = ['-G', '--generate-only']

    def update_the_repository(self) -> None:
        """ Updated the sbo repository. """
        if self.update == 0:
            self.view.question()
        else:
            print()

        if self.ponce_repo:

            if not self.is_option(self.flag_generate, self.flags):
                print('Updating the packages list.\n')
                print(f"Downloading the '{self.green}ponce{self.endc}' repository, please wait...\n")
                self.delete_file(self.ponce_repo_path, self.ponce_chglog_txt)
                lftp_output = subprocess.call(f'lftp {self.lftp_mirror_options} {self.ponce_repo_url} '
                                              f'{self.ponce_repo_path}', shell=True)
                self.process_error(lftp_output)

            # Remove the SLACKBUILDS.TXT file before generating the new one.
            sbo_file_txt = Path(self.ponce_repo_path, self.ponce_txt)
            if sbo_file_txt.is_file():
                sbo_file_txt.unlink()

            # Generating the ponce SLACKBUILDS.TXT file.
            print(f'Generating the {self.ponce_txt} file... ', end='', flush=True)
            os.chdir(self.ponce_repo_path)
            gen_output = subprocess.call(f'./gen_sbo_txt.sh > {self.ponce_txt}', shell=True)
            self.process_error(gen_output)
            print('\n')

        else:
            print('Updating the packages list.\n')

            self.delete_file(self.sbo_repo_path, self.sbo_txt)
            self.delete_file(self.sbo_repo_path, self.sbo_chglog_txt)

            print(f"Downloading the '{self.green}sbo{self.endc}' repository, please wait...\n")
            lftp_output = subprocess.call(f'lftp {self.lftp_mirror_options} {self.sbo_repo_url} '
                                          f'{self.sbo_repo_path}', shell=True)
            self.process_error(lftp_output)

        self.delete_sbo_data()
        data = CreateData()
        data.install_sbo_table()

    @staticmethod
    def process_error(output: int):
        if output != 0:
            raise SystemExit(output)

    def check(self, q) -> None:
        check_updates = CheckUpdates()
        is_update: int = 0
        if not check_updates.check():
            print(f'\n\n{self.endc}{self.yellow}No changes in ChangeLog.txt between your '
                  f'last update and now.{self.endc}')
        else:
            print(f'\n\n{self.bgreen}There are new updates available!{self.endc}')
            is_update: int = 1

        return q.put(is_update)

    def repository(self) -> None:
        """ Starting multiprocessing download process. """
        queue = Queue()
        message = f'Checking for news in the Changelog.txt file...'

        # Starting multiprocessing
        p1 = Process(target=self.check, args=(queue,))
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
        print('\x1b[?25h', self.endc, end='')

        self.update = queue.get()
        self.update_the_repository()

    @staticmethod
    def delete_file(folder: str, txt_file: str) -> None:
        """ Delete the file. """
        file = Path(folder, txt_file)
        if file.exists():
            file.unlink()

    def delete_sbo_data(self) -> None:
        """ Delete all the data from a table of the database. """
        if self.ponce_repo:
            self.session.query(PonceTable).delete()
        else:
            self.session.query(SBoTable).delete()
        self.session.commit()

    def drop_the_tables(self):
        """ Drop all the tables from the database. """
        print('All the data from the database will be deleted.')
        self.view.question()

        tables: list = [PonceTable.__table__,
                        SBoTable.__table__]

        Base.metadata.drop_all(bind=engine, tables=tables)
        print("Successfully cleared!\n\nYou need to run 'slpkg update' now.")
