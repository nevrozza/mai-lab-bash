import shlex

from colorama import init, Fore

from src.commands.import_default_commands import import_default_commands
from src.terminal.autocomplete import Autocomplete
from src.terminal.command import BashCommand
from src.terminal.file_system.fs import fs
from src.core.config import BashConfig
from src.core.errors import BashSyntaxError, BashError
from src.core.logging import shell_logger, log


# https://docs-python.ru/standart-library/modul-readline-python/
class Terminal:
    def __init__(self):
        # Импоритруем дефолтные команды (если в конфиге они включены)
        BashConfig.enable_default_commands and import_default_commands()
        # Enable autocomplete
        Autocomplete.enable()

    def cycle_input(self):
        init()  # Colorama
        fs.cd("~/Desktop")  # Start from ~/Desktop

        print("=== Double `Tab` to show all commands ===")
        while True:
            input_line = input(
                f"{Fore.LIGHTGREEN_EX}meow@user{Fore.RESET}:{Fore.LIGHTBLUE_EX}{fs.cwd_str()}{Fore.RESET}$ "
            )
            log(f"> {fs.cwd_str()}$ {input_line}", console_output=False)
            commands = self._parse_commands(input_line)
            self._execute_commands(commands)

    @staticmethod
    def _execute_commands(commands: list[BashCommand]):
        for command in commands:
            try:
                not_critical_errors, output = command.execute()
                if not_critical_errors:
                    for error in not_critical_errors:
                        log(error)
                output and log(output)
            except BashError as output:
                log(output)

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
                    log(f"'{name}' command not found")
        except BashSyntaxError as e:
            log(e)
        return commands

    @staticmethod
    def _get_command_raw_params(command: str) -> tuple[str, list[str]]:
        try:
            params = shlex.split(command)
            name = params[0]
            etc = params[1:]
            return name, etc
        except IndexError, ValueError:
            raise BashSyntaxError
