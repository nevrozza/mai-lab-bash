import shlex

from src.core.errors import BashSyntaxError


def get_command_raw_params(command: str) -> tuple[str, list[str]]:
    try:
        params = shlex.split(command)
        name = params[0]
        etc = params[1:]
        return name, etc
    except IndexError, ValueError:
        raise BashSyntaxError
