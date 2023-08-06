#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
import shutil
from pathlib import Path

from slpkg.configs import Configs
from slpkg.queries import SBoQueries
from slpkg.utilities import Utilities
from slpkg.downloader import Downloader
from slpkg.views.views import ViewMessage
from slpkg.models.models import session as Session


class Download(Configs, Utilities):
    """ Download the slackbuilds with the sources only. """

    def __init__(self, directory: str, flags: list):
        super(Configs, self).__init__()
        super(Utilities, self).__init__()
        self.flags: list = flags
        self.directory: str = directory

        self.session = Session

        self.flag_directory: list = ['-z=', '--directory=']

    def packages(self, slackbuilds: list) -> None:
        """ Download the package only. """
        view = ViewMessage(self.flags)
        view.download_packages(slackbuilds, self.directory)
        view.question()

        download_path: str = self.download_only_path
        if self.is_option(self.flag_directory, self.flags):
            download_path: str = self.directory

        start: float = time.time()
        for sbo in slackbuilds:
            file: str = f'{sbo}{self.sbo_tar_suffix}'
            location: str = SBoQueries(sbo).location()
            url: list = [f'{self.sbo_repo_url}{location}/{file}']

            if self.ponce_repo:
                ponce_repo_path_package = Path(self.ponce_repo_path, location, sbo)
                shutil.copytree(ponce_repo_path_package, f'{download_path}{sbo}')
            else:
                down_sbo = Downloader(download_path, url, self.flags)
                down_sbo.download()

            sources = SBoQueries(sbo).sources()
            down_source = Downloader(download_path, sources, self.flags)
            down_source.download()

        elapsed_time: float = time.time() - start
        self.finished_time(elapsed_time)
