#!/usr/bin/python3
# -*- coding: utf-8 -*-

from pathlib import Path

from slpkg.configs import Configs
from slpkg.queries import SBoQueries
from slpkg.utilities import Utilities
from slpkg.models.models import session as Session
from slpkg.models.models import SBoTable, PonceTable


class ViewPackage(Configs, Utilities):
    """ View the repository packages. """

    def __init__(self, flags: list):
        super(Configs, self).__init__()
        super(Utilities, self).__init__()
        self.flags: list = flags

        self.session = Session
        self.flag_pkg_version: list = ['-p', '--pkg-version']

        # Switch between sbo and ponce repository.
        self.sbo_table = SBoTable
        self.repo_url: str = self.sbo_repo_url
        self.repo_path: str = self.sbo_repo_path
        self.repo_tar_suffix: str = self.sbo_tar_suffix
        if self.ponce_repo:
            self.sbo_table = PonceTable
            self.repo_url: str = self.ponce_repo_url
            self.repo_path: str = self.ponce_repo_path
            self.repo_tar_suffix: str = ''

    def package(self, packages: list) -> None:
        """ View the packages from the repository. """
        color = self.colour()
        green: str = color['green']
        blue: str = color['blue']
        yellow: str = color['yellow']
        cyan: str = color['cyan']
        red: str = color['red']
        endc: str = color['endc']

        for package in packages:

            info: list = self.session.query(
                self.sbo_table.name,  # type: ignore
                self.sbo_table.version,  # type: ignore
                self.sbo_table.requires,  # type: ignore
                self.sbo_table.download,  # type: ignore
                self.sbo_table.download64,  # type: ignore
                self.sbo_table.md5sum,  # type: ignore
                self.sbo_table.md5sum64,  # type: ignore
                self.sbo_table.files,  # type: ignore
                self.sbo_table.short_description,  # type: ignore
                self.sbo_table.location  # type: ignore
            ).filter(self.sbo_table.name == package).first()

            path = Path(self.repo_path, info[9], info[0], 'README')
            readme = self.read_file(path)

            path = Path(self.repo_path, info[9], info[0], f'{info[0]}.info')
            info_file = self.read_file(path)

            repo_build_tag = self.read_build_tag(info[0])

            maintainer, email, homepage = '', '', ''
            for line in info_file:  # type: ignore
                if line.startswith('HOMEPAGE'):
                    homepage: str = line[10:-2].strip()
                if line.startswith('MAINTAINER'):
                    maintainer: str = line[12:-2].strip()
                if line.startswith('EMAIL'):
                    email: str = line[7:-2].strip()

            deps: str = (', '.join([f'{cyan}{pkg}' for pkg in info[2].split()]))

            if self.is_option(self.flag_pkg_version, self.flags):
                deps: str = (', '.join([f'{cyan}{pkg}{endc}-{yellow}{SBoQueries(pkg).version()}'
                             f'{green}' for pkg in info[2].split()]))

            print(f'Name: {green}{info[0]}{endc}\n'
                  f'Version: {green}{info[1]}{endc}\n'
                  f'Build: {green}{repo_build_tag}{endc}\n'
                  f'Requires: {green}{deps}{endc}\n'
                  f'Homepage: {blue}{homepage}{endc}\n'
                  f'Download SlackBuild: {blue}{self.repo_url}{info[9]}/{info[0]}'
                  f'{self.repo_tar_suffix}{endc}\n'
                  f'Download sources: {blue}{info[3]}{endc}\n'
                  f'Download_x86_64 sources: {blue}{info[4]}{endc}\n'
                  f'Md5sum: {yellow}{info[5]}{endc}\n'
                  f'Md5sum_x86_64: {yellow}{info[6]}{endc}\n'
                  f'Files: {green}{info[7]}{endc}\n'
                  f'Description: {green}{info[8]}{endc}\n'
                  f'Slackware: {cyan}{self.repo_url.split("/")[-1]}{endc}\n'
                  f'Category: {red}{info[9]}{endc}\n'
                  f'SBo url: {blue}{self.repo_url}{info[9]}/{info[0]}{endc}\n'
                  f'Maintainer: {yellow}{maintainer}{endc}\n'
                  f'Email: {yellow}{email}{endc}\n'
                  f'\nREADME: {cyan}{"".join(readme)}{endc}')  # type: ignore
