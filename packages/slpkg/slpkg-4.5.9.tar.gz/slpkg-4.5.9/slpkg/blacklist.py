#!/usr/bin/python3
# -*- coding: utf-8 -*-

import tomli
from pathlib import Path

from slpkg.configs import Configs
from slpkg.models.models import session as Session


class Blacklist(Configs):
    """ Reads and returns the blacklist. """

    def __init__(self):
        super(Configs, self).__init__()
        self.session = Session

    def packages(self) -> list:
        """ Reads the blacklist file. """
        file_toml = Path(self.etc_path, 'blacklist.toml')

        if file_toml.is_file():
            try:
                with open(file_toml, 'rb') as black:
                    return tomli.load(black)['BLACKLIST']['PACKAGES']
            except (tomli.TOMLDecodeError, KeyError) as error:
                raise SystemExit(f"\nError: {error}: in the configuration file '/etc/slpkg/blacklist.toml'.\n"
                                 f"\nIf you have upgraded the '{self.prog_name}' probably you need to run:\n"
                                 f"'mv {self.etc_path}/blacklist.toml.new {self.etc_path}/blacklist.toml'.\n")
        return []
