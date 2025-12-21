import logging

from src.core.config import BashConfig
from src.terminal.file_system.resolve_path import resolve_path


class ShellFormatter(logging.Formatter):
    def format(self, record):
        if record.levelno == logging.INFO:
            record.levelname = ""
        elif record.levelno == logging.ERROR:
            record.levelname = r"ERROR: "
        return super().format(record)


class Logger:

    @classmethod
    def setup_shell_logger(cls):
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
        logger = logging.getLogger("shell_logger")
        logger.setLevel(logging.INFO)

        file = logging.FileHandler(resolve_path(BashConfig.LOGS_FILE_NAME), mode="w", encoding="utf-8")

        file_formatter = ShellFormatter("[%(asctime)s] %(levelname)s%(message)s",
                                        datefmt="%Y-%m-%d %H:%M:%S")
        file.setFormatter(file_formatter)

        logger.addHandler(file)
        cls.shell_logger = logger

    @classmethod
    def error(cls, message):
        cls.shell_logger.error(message)

    @classmethod
    def info(cls, message):
        cls.shell_logger.info(message)


def log(output: str | Exception, console_output: bool = True, file_output: bool = True):
    console_output and print(output)
    if isinstance(output, Exception):
        file_output and Logger.error(output)
    else:
        file_output and Logger.info(output)
