import pathlib
import readline
import shlex

from colorama import init, Fore

from src.terminal.autocomplete import Autocomplete
from src.terminal.command import BashCommand
from src.terminal.fs import FS
from src.utils.errors import BashSyntaxError


# https://docs-python.ru/standart-library/modul-readline-python/
class Terminal:
    def __init__(self):
        # Импоритруем команды
        BashCommand.import_all_commands()
        # Enable autocomplete
        Autocomplete.enable()

    def cycle_input(self):
        init()  # Colorama
        FS.cd("~/Desktop")  # Start from ~/Desktop

        print("=== Double `Tab` to show all commands ===")
        while True:
            input_line = input(
                f"{Fore.LIGHTGREEN_EX}meow@user{Fore.RESET}:{Fore.LIGHTBLUE_EX}{FS.cwd_str()}{Fore.RESET}$ "
            )
            commands = self._parse_commands(input_line)
            self._execute_commands(commands)

    @staticmethod
    def _execute_commands(commands: list[BashCommand]):
        for command in commands:
            command.execute()

    @classmethod
    def _parse_commands(cls, input_line: str) -> list[BashCommand]:
        commands: list[BashCommand] = []
        try:
            raw_parametrized_commands = [cls._get_command_raw_params(command) for command in input_line.split(";") if
                                         command.strip()]
            for name, raw_params in raw_parametrized_commands:
                try:
                    command = BashCommand.get_command(name)
                    commands.append(command(raw_params))
                except KeyError:
                    print(f"'{name}' command not found")
        except BashSyntaxError:
            print(f"syntax error!")
        return commands

    @staticmethod
    def _get_command_raw_params(command: str) -> tuple[str, list[str]]:
        try:
            params = shlex.split(command)
            name = params[0]
            etc = params[1:]
            return name, etc
        except IndexError:
            raise BashSyntaxError
