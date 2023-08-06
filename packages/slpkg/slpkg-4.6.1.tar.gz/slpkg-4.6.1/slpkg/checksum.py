#!/usr/bin/python3
# -*- coding: utf-8 -*-

import hashlib
from pathlib import Path
from typing import Union
from urllib.parse import unquote

from slpkg.views.ascii import Ascii
from slpkg.views.views import ViewMessage


class Md5sum:
    """ Checksum the sources. """

    def __init__(self, flags: list):
        self.flags: list = flags
        self.ascii = Ascii()

    def check(self, path: Union[str, Path], source: str, checksum: str) -> None:
        """ Checksum the source. """
        source_file = unquote(source)
        filename = source_file.split('/')[-1]
        source_path = Path(path, filename)

        md5 = self.read_file(source_path)

        file_check = hashlib.md5(md5).hexdigest()

        checksum = "".join(checksum)

        if file_check != checksum:
            self.ascii.draw_checksum_error_box(filename, checksum, file_check)
            view = ViewMessage(self.flags)
            view.question()

    @staticmethod
    def read_file(filename: Union[str, Path]) -> bytes:
        """ Reads the text file. """
        with open(filename, 'rb') as f:
            return f.read()
