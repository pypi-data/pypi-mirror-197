#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
from pathlib import Path

from slpkg.checks import Check
from slpkg.upgrade import Upgrade
from slpkg.configs import Configs
from slpkg.tracking import Tracking
from slpkg.queries import SBoQueries
from slpkg.dependees import Dependees
from slpkg.utilities import Utilities
from slpkg.search import SearchPackage
from slpkg.views.cli_menu import Usage
from slpkg.dialog_box import DialogBox
from slpkg.views.version import Version
from slpkg.download_only import Download
from slpkg.slackbuild import Slackbuilds
from slpkg.views.views import ViewMessage
from slpkg.form_configs import FormConfigs
from slpkg.views.help_commands import Help
from slpkg.check_updates import CheckUpdates
from slpkg.find_installed import FindInstalled
from slpkg.views.view_package import ViewPackage
from slpkg.remove_packages import RemovePackages
from slpkg.clean_logs import CleanLogsDependencies
from slpkg.update_repository import UpdateRepository


class Argparse(Configs):

    def __init__(self, args: list):
        super(Configs).__init__()
        self.args: list = args
        self.flags: list = []
        self.directory = self.tmp_slpkg
        self.dialogbox = DialogBox()
        self.utils = Utilities()
        self.usage = Usage()
        self.check = Check()
        self.form_configs = FormConfigs()
        self.color = self.colour()

        self.bold: str = self.color['bold']
        self.red: str = self.color['red']
        self.endc: str = self.color['endc']
        self.bred: str = f'{self.bold}{self.red}'

        self.file_pattern: str = f'*{self.repo_tag}'
        if self.file_pattern_conf:
            self.file_pattern = self.file_pattern_conf

        if len(self.args) == 0:
            self.usage.help_short()

        self.check.blacklist(self.args)

        self.flag_yes: str = '--yes'
        self.flag_short_yes: str = '-y'
        self.flag_jobs: str = '--jobs'
        self.flag_short_jobs: str = '-j'
        self.flag_resolve_off: str = '--resolve-off'
        self.flag_short_resolve_off: str = '-o'
        self.flag_reinstall: str = '--reinstall'
        self.flag_short_reinstall: str = '-r'
        self.flag_skip_installed: str = '--skip-installed'
        self.flag_short_skip_installed: str = '-k'
        self.flag_full_reverse: str = '--full-reverse'
        self.flag_short_full_reverse: str = '-E'
        self.flag_search: str = '--search'
        self.flag_short_search: str = '-S'
        self.flag_no_silent: str = '--no-silent'
        self.flag_short_no_silent: str = '-n'
        self.flag_pkg_version: str = '--pkg-version'
        self.flag_short_pkg_version: str = '-p'
        self.flag_generate: str = '--generate-only'
        self.flag_short_generate: str = '-G'
        self.flag_parallel: str = '--parallel'
        self.flag_short_parallel: str = '-P'
        self.flag_directory: str = '--directory='
        self.flag_short_directory: str = '-z='
        self.flag_file_pattern: str = '--file-pattern='
        self.flag_short_file_pattern: str = '-F='

        self.flag_searches: list = [self.flag_short_search, self.flag_search]

        self.options: list = [
            self.flag_yes,
            self.flag_short_yes,
            self.flag_jobs,
            self.flag_short_jobs,
            self.flag_resolve_off,
            self.flag_short_resolve_off,
            self.flag_reinstall,
            self.flag_short_reinstall,
            self.flag_skip_installed,
            self.flag_short_skip_installed,
            self.flag_full_reverse,
            self.flag_short_full_reverse,
            self.flag_search,
            self.flag_short_search,
            self.flag_no_silent,
            self.flag_short_no_silent,
            self.flag_pkg_version,
            self.flag_short_pkg_version,
            self.flag_generate,
            self.flag_short_generate,
            self.flag_parallel,
            self.flag_short_parallel,
            self.flag_directory,
            self.flag_short_directory,
            self.flag_file_pattern,
            self.flag_short_file_pattern
        ]
        
        self.commands: dict = {
            '--help': [],
            '--version': [],
            'help': [],
            'update': [
                self.flag_yes,
                self.flag_short_yes,
                self.flag_generate,
                self.flag_short_generate,
                self.flag_parallel,
                self.flag_short_parallel,
            ],
            'upgrade': [
                self.flag_yes,
                self.flag_short_yes,
                self.flag_jobs,
                self.flag_short_jobs,
                self.flag_resolve_off,
                self.flag_short_resolve_off,
                self.flag_reinstall,
                self.flag_short_reinstall,
                self.flag_no_silent,
                self.flag_short_no_silent,
                self.flag_file_pattern,
                self.flag_short_file_pattern,
                self.flag_parallel,
                self.flag_short_parallel,
            ],
            'check-updates': [],
            'configs': [],
            'clean-logs': [
                self.flag_yes,
                self.flag_short_yes
            ],
            'clean-data': [
                self.flag_yes,
                self.flag_short_yes
            ],
            'clean-tmp': [],
            'build': [
                self.flag_yes,
                self.flag_short_yes,
                self.flag_jobs,
                self.flag_short_jobs,
                self.flag_resolve_off,
                self.flag_short_resolve_off,
                self.flag_search,
                self.flag_short_search,
                self.flag_no_silent,
                self.flag_short_no_silent,
                self.flag_parallel,
                self.flag_short_parallel,
            ],
            'install': [
                self.flag_yes,
                self.flag_short_yes,
                self.flag_jobs,
                self.flag_short_jobs,
                self.flag_resolve_off,
                self.flag_short_resolve_off,
                self.flag_reinstall,
                self.flag_short_reinstall,
                self.flag_skip_installed,
                self.flag_short_skip_installed,
                self.flag_search,
                self.flag_short_search,
                self.flag_no_silent,
                self.flag_short_no_silent,
                self.flag_file_pattern,
                self.flag_short_file_pattern,
                self.flag_parallel,
                self.flag_short_parallel,
            ],
            'download': [
                self.flag_yes,
                self.flag_short_yes,
                self.flag_search,
                self.flag_short_search,
                self.flag_no_silent,
                self.flag_short_no_silent,
                self.flag_directory,
                self.flag_short_directory,
                self.flag_parallel,
                self.flag_short_parallel,
            ],
            'remove': [
                self.flag_resolve_off,
                self.flag_short_resolve_off,
                self.flag_search,
                self.flag_short_search,
                self.flag_no_silent,
                self.flag_short_no_silent,
                self.flag_file_pattern,
                self.flag_short_file_pattern
            ],
            'find': [
                self.flag_search,
                self.flag_short_search,
                self.flag_file_pattern,
                self.flag_short_file_pattern
            ],
            'view': [
                self.flag_search,
                self.flag_short_search,
                self.flag_pkg_version,
                self.flag_short_pkg_version
            ],
            'search': [
                self.flag_search,
                self.flag_short_search,
            ],
            'dependees': [
                self.flag_full_reverse,
                self.flag_short_full_reverse,
                self.flag_search,
                self.flag_short_search,
                self.flag_pkg_version,
                self.flag_short_pkg_version
            ],
            'tracking': [
                self.flag_search,
                self.flag_short_search,
                self.flag_pkg_version,
                self.flag_short_pkg_version
            ]
        }

        self.commands['-h'] = self.commands['--help']
        self.commands['-v'] = self.commands['--version']
        self.commands['-u'] = self.commands['update']
        self.commands['-U'] = self.commands['upgrade']
        self.commands['-c'] = self.commands['check-updates']
        self.commands['-g'] = self.commands['configs']
        self.commands['-L'] = self.commands['clean-logs']
        self.commands['-D'] = self.commands['clean-tmp']
        self.commands['-T'] = self.commands['clean-data']
        self.commands['-b'] = self.commands['build']
        self.commands['-i'] = self.commands['install']
        self.commands['-d'] = self.commands['download']
        self.commands['-R'] = self.commands['remove']
        self.commands['-f'] = self.commands['find']
        self.commands['-w'] = self.commands['view']
        self.commands['-s'] = self.commands['search']
        self.commands['-e'] = self.commands['dependees']
        self.commands['-t'] = self.commands['tracking']

        self.split_options()
        self.split_options_from_args()
        self.move_options()

    def split_options(self) -> None:
        """ Split options and commands, like: -iyjR

            slpkg -jyiR package

            Puts the command first and options after.
            Result: ['-i', '-y', '-j', '-R']
        """
        for args in self.args:
            if args[0] == '-' and args[:2] != '--' and len(args) >= 3 and '=' not in args:
                self.args.remove(args)

                for opt in list(map(lambda item: f'-{item}', [arg for arg in list(args[1:])])):
                    if opt in self.commands.keys():
                        self.args.insert(0, opt)
                        continue

                    self.args.append(opt)

    def split_options_from_args(self) -> None:
        """ Split options from arguments.

            slpkg -f package --file-pattern='*'

            Splits the option ['--file-pattern'] and ['*']
        """
        for arg in self.args:
            if arg.startswith(self.flag_directory):
                self.directory = arg.split('=')[1]
                self.args[self.args.index(arg)] = self.flag_directory

            if arg.startswith(self.flag_short_directory):
                self.directory = arg.split('=')[1]
                self.args[self.args.index(arg)] = self.flag_short_directory

            if arg.startswith(self.flag_file_pattern):
                self.file_pattern = arg.split('=')[1]
                self.args[self.args.index(arg)] = self.flag_file_pattern

            if arg.startswith(self.flag_short_file_pattern):
                self.file_pattern = arg.split('=')[1]
                self.args[self.args.index(arg)] = self.flag_short_file_pattern

    def move_options(self) -> None:
        """ Move options to the flags and removes from the arguments. """
        for opt in self.options:
            if opt in self.args:
                self.args.remove(opt)
                self.flags.append(opt)

    def check_for_flags(self, command: str) -> None:
        """ Check for correct flags. """
        flags: list = self.commands[command]

        for opt in self.flags:
            if opt not in flags and opt not in ['--help', '--version']:
                self.usage.error_for_options(command, flags)

    def is_file_list_packages(self):
        """ Checks if the arg is filelist.pkgs. """
        if self.args[1].endswith(self.file_list_suffix):
            file = Path(self.args[1])
            packages: list = list(self.utils.read_packages_from_file(file))
        else:
            packages: list = list(set(self.args[1:]))

        return packages

    def choose_packages(self, packages: list, method: str) -> list:
        """ Choose packages with dialog utility and -S, --search flag. """
        height: int = 10
        width: int = 70
        list_height: int = 0
        choices: list = []
        title: str = f' Choose packages you want to {method} '
        repo_packages: list = SBoQueries('').sbos()

        installed: list = list(self.utils.all_installed(self.file_pattern))

        if method in ['remove', 'find']:

            for package in installed:
                name: str = self.utils.split_installed_pkg(package)[0]
                version: str = self.utils.split_installed_pkg(package)[1]

                for pkg in packages:
                    if pkg in name:
                        choices += [(name, version, False, f'Package: {package}')]

        elif method == 'upgrade':
            for pkg in packages:
                for package in repo_packages:

                    if pkg == package:
                        repo_ver: str = SBoQueries(package).version()
                        inst_pkg: str = self.utils.is_package_installed(package, self.file_pattern)
                        inst_ver: str = self.utils.split_installed_pkg(inst_pkg)[1]

                        repo_build_tag = self.utils.read_build_tag(package)
                        inst_build_tag = self.utils.split_installed_pkg(inst_pkg)[3]

                        choices += [(package, f'{inst_ver} -> {repo_ver}', True,
                                     f'Installed: {package}-{inst_ver} Build: {inst_build_tag} -> '
                                     f'Available: {repo_ver} Build: {repo_build_tag}')]

        else:
            for pkg in packages:
                for package in repo_packages:

                    if pkg in package:
                        repo_ver = SBoQueries(package).version()
                        choices += [(package, repo_ver, False, f'Package: {package}-{repo_ver}')]

        if not choices:
            return packages

        text: str = f'There are {len(choices)} packages:'
        code, tags = self.dialogbox.checklist(text, packages, title, height,
                                              width, list_height, choices)

        if not code:
            return packages

        os.system('clear')

        if not tags:
            raise SystemExit()

        return tags

    def help(self) -> None:
        if len(self.args) == 1:
            self.usage.help(0)
        self.usage.help(1)

    def version(self) -> None:
        if len(self.args) == 1:
            version = Version()
            version.view()
            raise SystemExit()
        self.usage.help(1)

    def update(self) -> None:
        if len(self.args) == 1:
            update = UpdateRepository(self.flags)
            update.repository()
            raise SystemExit()
        self.usage.help(1)

    def upgrade(self) -> None:
        command = Argparse.upgrade.__name__

        if len(self.args) == 1:
            self.check.database()

            upgrade = Upgrade(self.file_pattern)
            packages: list = list(upgrade.packages())

            packages: list = self.choose_packages(packages, command)

            if not packages:
                print('\nEverything is up-to-date.\n')
                raise SystemExit()

            install = Slackbuilds(packages, self.flags, self.file_pattern, mode=command)
            install.execute()
            raise SystemExit()
        self.usage.help(1)

    def check_updates(self) -> None:
        if len(self.args) == 1:
            self.check.database()
            check = CheckUpdates()
            check.updates()
            raise SystemExit()
        self.usage.help(1)

    def edit_configs(self) -> None:
        if len(self.args) == 1:
            self.form_configs.edit()
            raise SystemExit()
        self.usage.help(1)

    def new_configs(self) -> None:
        if len(self.args) == 1:
            new_config = NewConfig()
            new_config.check()
            raise SystemExit()
        self.usage.help(1)

    def clean_logs(self) -> None:
        if len(self.args) == 1:
            self.check.database()

            logs = CleanLogsDependencies(self.flags)
            logs.clean()
            raise SystemExit()
        self.usage.help(1)

    def clean_tmp(self) -> None:
        if len(self.args) == 1:

            print(f"\n[{self.bred}WARNING{self.endc}]: All the files in the '{self.tmp_path}{self.prog_name}' "
                  f"folder will delete!")

            views = ViewMessage(self.flags)
            views.question()

            self.utils.remove_folder_if_exists(path=self.tmp_path, folder=self.prog_name)
            self.utils.create_folder(path=self.tmp_slpkg, folder='build')
            print(f"The folder '{self.tmp_path}{self.prog_name}' was cleaned!")

            raise SystemExit()
        self.usage.help(1)

    def clean_data(self) -> None:
        if len(self.args) == 1:
            update = UpdateRepository(self.flags)
            update.drop_the_tables()
            raise SystemExit()
        self.usage.help(1)

    def build(self) -> None:
        command = Argparse.build.__name__

        if len(self.args) >= 2:

            packages: list = self.is_file_list_packages()

            if self.utils.is_option(self.flag_searches, self.flags):
                packages: list = self.choose_packages(packages, command)

            self.check.database()
            packages: list = self.check.exists(packages)
            self.check.unsupported(packages)

            build = Slackbuilds(packages, self.flags, self.file_pattern, mode=command)
            build.execute()
            raise SystemExit()
        self.usage.help(1)

    def install(self) -> None:
        command = Argparse.install.__name__

        if len(self.args) >= 2:

            packages: list = self.is_file_list_packages()

            if self.utils.is_option(self.flag_searches, self.flags):
                packages: list = self.choose_packages(packages, command)

            self.check.database()
            packages: list = self.check.exists(packages)
            self.check.unsupported(packages)

            install = Slackbuilds(packages, self.flags, self.file_pattern, mode=command)
            install.execute()
            raise SystemExit()
        self.usage.help(1)

    def download(self) -> None:
        command = Argparse.download.__name__

        if len(self.args) >= 2:

            packages: list = self.is_file_list_packages()

            if self.utils.is_option(self.flag_searches, self.flags):
                packages: list = self.choose_packages(packages, command)

            self.check.database()
            packages: list = self.check.exists(packages)
            download = Download(self.directory, self.flags)
            download.packages(packages)
            raise SystemExit()
        self.usage.help(1)

    def remove(self) -> None:
        command = Argparse.remove.__name__

        if len(self.args) >= 2:

            packages: list = self.is_file_list_packages()

            if self.utils.is_option(self.flag_searches, self.flags):
                packages: list = self.choose_packages(packages, command)

            self.check.database()
            packages: list = self.check.installed(packages, self.file_pattern)

            remove = RemovePackages(packages, self.flags, self.file_pattern)
            remove.remove()
            raise SystemExit()
        self.usage.help(1)

    def find(self) -> None:
        command = Argparse.find.__name__

        if len(self.args) >= 2:

            packages: list = self.is_file_list_packages()

            if self.utils.is_option(self.flag_searches, self.flags):
                packages: list = self.choose_packages(packages, command)

            self.check.database()

            find = FindInstalled()
            find.find(packages, self.file_pattern)
            raise SystemExit()
        self.usage.help(1)

    def view(self) -> None:
        command = Argparse.view.__name__

        if len(self.args) >= 2:

            packages: list = self.is_file_list_packages()

            if self.utils.is_option(self.flag_searches, self.flags):
                packages: list = self.choose_packages(packages, command)

            self.check.database()
            packages: list = self.check.exists(packages)

            view = ViewPackage(self.flags)
            view.package(packages)
            raise SystemExit()
        self.usage.help(1)

    def search(self) -> None:
        command = Argparse.search.__name__

        if len(self.args) >= 2:

            packages: list = self.is_file_list_packages()

            if self.utils.is_option(self.flag_searches, self.flags):
                packages: list = self.choose_packages(packages, command)

            self.check.database()

            search = SearchPackage()
            search.package(packages)
            raise SystemExit()
        self.usage.help(1)

    def dependees(self) -> None:
        command = Argparse.dependees.__name__

        if len(self.args) >= 2:

            packages: list = self.is_file_list_packages()

            if self.utils.is_option(self.flag_searches, self.flags):
                packages: list = self.choose_packages(packages, command)

            self.check.database()
            packages: list = self.check.exists(packages)

            dependees = Dependees(packages, self.flags)
            dependees.slackbuilds()
            raise SystemExit()
        self.usage.help(1)

    def tracking(self) -> None:
        command = Argparse.tracking.__name__

        if len(self.args) >= 2:

            packages: list = self.is_file_list_packages()

            if self.utils.is_option(self.flag_searches, self.flags):
                packages: list = self.choose_packages(packages, command)

            self.check.database()
            packages: list = self.check.exists(packages)

            tracking = Tracking(self.flags)
            tracking.packages(packages)
            raise SystemExit()
        self.usage.help(1)

    def help_for_commands(self) -> None:
        """ Extra help information for commands. """
        if len(self.args) == 2:
            flags = self.commands[self.args[1]]
            Help(self.args[1], flags).view()
        else:
            self.usage.help(1)


def main():
    args = sys.argv
    args.pop(0)

    argparse = Argparse(args)

    arguments: dict = {
        '-h': argparse.help,
        '--help': argparse.help,
        '-v': argparse.version,
        '--version': argparse.version,
        'help': argparse.help_for_commands,
        'update': argparse.update,
        '-u': argparse.update,
        'upgrade': argparse.upgrade,
        '-U': argparse.upgrade,
        'check-updates': argparse.check_updates,
        '-c': argparse.check_updates,
        'configs': argparse.edit_configs,
        '-g': argparse.edit_configs,
        'clean-logs': argparse.clean_logs,
        '-L': argparse.clean_logs,
        'clean-data': argparse.clean_data,
        '-T': argparse.clean_data,
        'clean-tmp': argparse.clean_tmp,
        '-D': argparse.clean_tmp,
        'build': argparse.build,
        '-b': argparse.build,
        'install': argparse.install,
        '-i': argparse.install,
        'download': argparse.download,
        '-d': argparse.download,
        'remove': argparse.remove,
        '-R': argparse.remove,
        'view': argparse.view,
        '-w': argparse.view,
        'find': argparse.find,
        '-f': argparse.find,
        'search': argparse.search,
        '-s': argparse.search,
        'dependees': argparse.dependees,
        '-e': argparse.dependees,
        'tracking': argparse.tracking,
        '-t': argparse.tracking
    }

    try:
        argparse.check_for_flags(args[0])
        arguments[args[0]]()
    except (KeyError, IndexError):
        Usage().help(1)


if __name__ == '__main__':
    main()
