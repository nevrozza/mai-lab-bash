from src.core.errors import BashError, BashNoSuchFileOrDirectory
from src.terminal.file_system.fs import fs


def validate_paths(
        params: list[str],
        command_name: str,
        if_no_params=None,
        on_not_existing=None
) -> list[BashError]:
    errors = []
    if not params:
        if_no_params or params.append(fs.cwd_str())
    else:
        for path in params[:]:  # copy
            if not fs.properties.existing_path(path):
                if on_not_existing:
                    on_not_existing(path)
                else:
                    params.remove(path)
                    errors.append(BashNoSuchFileOrDirectory(name=command_name, filename=path))
    return errors
