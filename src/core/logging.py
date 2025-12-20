import logging

from src.core.config import BashConfig


class ShellFormatter(logging.Formatter):
    def format(self, record):
        if record.levelno == logging.INFO:
            record.levelname = ""
        elif record.levelno == logging.ERROR:
            record.levelname = r"ERROR: "
        return super().format(record)


def setup_shell_logger():
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    logger = logging.getLogger("shell_logger")
    logger.setLevel(logging.INFO)

    file = logging.FileHandler(BashConfig.LOGS_FILE_NAME, mode="w", encoding="utf-8")

    file_formatter = ShellFormatter("[%(asctime)s] %(levelname)s%(message)s",
                                    datefmt="%Y-%m-%d %H:%M:%S")
    file.setFormatter(file_formatter)

    logger.addHandler(file)
    return logger


shell_logger = setup_shell_logger()


def log(output: str | Exception, console_output: bool = True, file_output: bool = True):
    console_output and print(output)
    if isinstance(output, Exception):
        file_output and shell_logger.error(output)
    else:
        file_output and shell_logger.info(output)
