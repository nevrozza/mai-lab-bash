from colorama import init, Fore

from src.commands.import_default_commands import import_default_commands
from src.core.config import BashConfig
from src.core.errors import BashSyntaxError, BashError
from src.core.logging import log
from src.terminal.autocomplete import Autocomplete
from src.terminal.command import BashCommand
from src.terminal.file_system.fs import fs
from src.terminal.history import HistoryManager
from src.utils.get_command_raw_params import get_command_raw_params


# https://docs-python.ru/standart-library/modul-readline-python/
class Terminal:
    """Основной цикл терминала: обработка ввода, разбор и выполнение команд, логгирование"""

    def __init__(self):
        # Импоритруем дефолтные команды (если в конфиге они включены)
        BashConfig.IMPORT_DEFAULT_COMMANDS and import_default_commands()
        # Enable autocomplete
        Autocomplete.enable()
        # Инициализируем историю команд
        HistoryManager.initialize()

    def cycle_input(self):
        """Бесконечный цикл ввода команд"""
        init()  # Colorama
        fs.cd("~/Desktop")  # Start from ~/Desktop

        print("=== Double `Tab` to show all commands ===")
        while True:
            try:
                input_line = input(
                    f"{Fore.LIGHTGREEN_EX}meow@user{Fore.RESET}:{Fore.LIGHTBLUE_EX}{fs.cwd_str()}{Fore.RESET}$ "
                )
                log(f"> {fs.cwd_str()}$ {input_line}", console_output=False)
                commands = self._parse_commands(input_line)
                self._execute_commands(commands)
            except KeyboardInterrupt:
                print("\nBye!")
                break

    @staticmethod
    def _execute_commands(commands: list[BashCommand]):
        """Выполняет список команд, логгирует и добавляет их в историю"""
        for command in commands:
            cwd = fs.cwd_str()
            is_error = False
            try:
                not_critical_validation_errors, (not_critical_exec_errors, output) = command.execute()
                not_critical_errors = (not_critical_validation_errors or []) + (not_critical_exec_errors or [])
                if not_critical_errors:
                    for error in not_critical_errors:
                        log(error)
                output and log(output)
                is_error = bool(not_critical_errors)
            except BashError as output:
                log(output)
                is_error = True
            finally:
                HistoryManager.add_command(command_name=command.name(), command_line=command.command_line,
                                           is_error=is_error, wd=cwd)

    @classmethod
    def _parse_commands(cls, input_line: str) -> list[BashCommand]:
        """Разбирает строку ввода на отдельные команды (разделённые ';'),
        парсит `сырые` параметры (вместе с флагами). Возвращает список BashCommand
        :return: list[BashCommand] – список команд"""
        cwd = fs.cwd_str()
        commands: list[BashCommand] = []
        try:
            for command_line in input_line.split(";"):
                if command_line.strip():
                    name, raw_params = get_command_raw_params(command_line)
                    try:
                        bash_command = BashCommand.get_command(name)
                        commands.append(bash_command(raw_params, command_line))
                    except KeyError:
                        HistoryManager.add_command(command_name=name, command_line=command_line, is_error=True, wd=cwd)
                        log(f"'{name}' command not found")
        except BashSyntaxError as e:
            log(e)
        return commands
