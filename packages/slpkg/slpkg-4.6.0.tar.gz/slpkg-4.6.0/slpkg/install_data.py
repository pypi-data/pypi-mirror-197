#!/usr/bin/python3
# -*- coding: utf-8 -*-

from pathlib import Path

from slpkg.configs import Configs
from slpkg.queries import SBoQueries
from slpkg.utilities import Utilities
from slpkg.models.models import session as Session
from slpkg.models.models import SBoTable, PonceTable


class CreateData(Configs):
    """ Reads the SLACKBUILDS.TXT file and inserts them into the database. """

    def __init__(self):
        super(Configs, self).__init__()

        self.session = Session
        self.utils = Utilities()
        self.query = SBoQueries('')

    def install_sbo_table(self) -> None:
        """ Install the data for SBo repository. """
        sbo_tags = [
            'SLACKBUILD NAME:',
            'SLACKBUILD LOCATION:',
            'SLACKBUILD FILES:',
            'SLACKBUILD VERSION:',
            'SLACKBUILD DOWNLOAD:',
            'SLACKBUILD DOWNLOAD_x86_64:',
            'SLACKBUILD MD5SUM:',
            'SLACKBUILD MD5SUM_x86_64:',
            'SLACKBUILD REQUIRES:',
            'SLACKBUILD SHORT DESCRIPTION:'
        ]
        sbo_table = SBoTable
        path = Path(self.sbo_repo_path, self.sbo_txt)

        if self.ponce_repo:
            sbo_table = PonceTable
            path = Path(self.ponce_repo_path, self.ponce_txt)

        sbo_file: list = self.utils.read_file(path)

        cache: list = []  # init cache

        print('Creating the database... ', end='', flush=True)

        for i, line in enumerate(sbo_file, 1):

            for tag in sbo_tags:
                if line.startswith(tag):
                    line = line.replace(tag, '').strip()
                    cache.append(line)

            if (i % 11) == 0:
                data: str = sbo_table(name=cache[0], location=cache[1].split('/')[1],
                                      files=cache[2], version=cache[3],
                                      download=cache[4], download64=cache[5],
                                      md5sum=cache[6], md5sum64=cache[7],
                                      requires=cache[8], short_description=cache[9])
                self.session.add(data)

                cache: list = []  # reset cache after 11 lines

        print('Done')

        self.session.commit()
