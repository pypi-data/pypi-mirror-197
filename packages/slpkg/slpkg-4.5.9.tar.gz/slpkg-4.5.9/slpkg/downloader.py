#!/usr/bin/python3
# -*- coding: utf-8 -*-

import subprocess
from typing import Union
from pathlib import Path
from urllib.parse import unquote
from multiprocessing import Process

from slpkg.configs import Configs
from slpkg.utilities import Utilities


class Downloader(Configs, Utilities):

    def __init__(self, path: Union[str, Path], urls: list, flags: list):
        super(Configs, self).__init__()
        super(Utilities, self).__init__()
        self.path = path
        self.urls: list = urls
        self.flags: list = flags

        self.color = self.colour()

        self.bold: str = self.color['bold']
        self.cyan: str = self.color['cyan']
        self.red: str = self.color['red']
        self.endc: str = self.color['endc']
        self.byellow: str = f'{self.bold}{self.yellow}'
        self.bred: str = f'{self.bold}{self.red}'
        self.flag_parallel: list = ['-P', '--parallel']

    def download(self):
        """ Starting the processing for downloading. """
        process: list = []

        if self.parallel_downloads or self.is_option(self.flag_parallel, self.flags):
            for url in self.urls:
                p1 = Process(target=self.tools, args=(url,))
                process.append(p1)
                p1.start()

            for proc in process:
                proc.join()
        else:
            for url in self.urls:
                self.tools(url)

    def tools(self, url: str) -> None:
        """ Downloader tools wget, curl and lftp. """
        filename: str = url.split('/')[-1]

        if self.downloader == 'wget':
            output = subprocess.call(f'{self.downloader} {self.wget_options} --directory-prefix={self.path} '
                                     f'"{url}"', shell=True)

        elif self.downloader == 'curl':
            output = subprocess.call(f'{self.downloader} {self.curl_options} "{url}" --output '
                                     f'{self.path}/{filename}', shell=True)

        elif self.downloader == 'lftp':
            output = subprocess.call(f'lftp {self.lftp_get_options} {url} -o {self.path}', shell=True)

        else:
            raise SystemExit(f"{self.red}Error:{self.endc} Downloader '{self.downloader}' not supported.\n")

        if output != 0:
            raise SystemExit(output)

        self.check_if_downloaded(url, output)

    def check_if_downloaded(self, url: str, output: int) -> None:
        """ Checks if the file downloaded. """
        url: str = unquote(url)
        file: str = url.split('/')[-1]
        path_file = Path(self.path, file)

        if not path_file.exists():
            raise SystemExit(f"\n{self.bred}FAILED {output}:{self.endc} Download the '{self.cyan}{file}{self.endc}' "
                             f"file.\n")
