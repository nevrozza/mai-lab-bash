from src.core.errors import BashError, BashMissingDestinationFileOperandError, BashMissingFileOperandError, \
    BashNoSuchFileOrDirectoryError, BashNotADirectoryError, BashCommandError
from src.terminal.file_system.fs import fs


def default_validate_params(
        params: list[str],
        if_no_params,
        validate_path,
) -> list[BashError]:
    """
    Общая валидация параметров: вызывает callback'и при отсутствии параметров и проверке каждого пути
    :param params: параметры
    :param validate_path: callback(path: str) на каждом параметре
    :param if_no_params: callback, если нет параметров
    """
    errors = []
    if not params:
        if_no_params and if_no_params()
    else:
        for path in params[:]:
            possible_error = validate_path(path)
            if isinstance(possible_error, BashError):
                errors.append(possible_error)
    return errors


def cp_mv_validate_params(
        params: list[str],
        command_name: str,
        allow_dirs: bool,
):
    """Валидация параметров для cp/mv с учётом количества аргументов и типа (файл/директория)"""
    if len(params) == 1:
        raise BashMissingDestinationFileOperandError(name=command_name, prev_path=params[0])
    elif len(params) == 0:
        raise BashMissingFileOperandError(command_name)

    path_index = 0

    def validate_path(path: str):
        nonlocal path_index
        if (path_index + 1) < len(params):  # check no destination
            if not fs.properties.existing_path(path):
                raise BashNoSuchFileOrDirectoryError(name=command_name, filename=path)
            elif fs.properties.is_dir(path) and (not allow_dirs):
                raise BashCommandError(command_name, msg="-r not specified")
        if len(params) > 2 and path_index == (len(params) - 1):  # cp/mv file1 file2 dir
            if not fs.properties.existing_path(path):
                raise BashNoSuchFileOrDirectoryError(name=command_name, filename=path)
            elif not fs.properties.is_dir(path):
                raise BashNotADirectoryError(name=command_name, filename=path)
        path_index += 1

    for pathx in params:
        validate_path(pathx)
    return []
