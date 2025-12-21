import pathlib
import stat
from dataclasses import dataclass


@dataclass(frozen=True)
class PathDetails:
    path: pathlib.Path
    permissions: str
    blocks: int
    owner: str
    group: str
    size: int
    modification_time: str
    name: str


def get_permission_string(path: pathlib.Path) -> str:
    """:return: Строка прав доступа (пример: `-rwxr-xr--`)."""
    mode = path.stat().st_mode
    # not fs because of circular import..
    type = "d" if path.is_dir() else "-"
    # https://stackoverflow.com/questions/16249440/changing-file-permission-in-python
    permissions = [
        'r' if mode & stat.S_IRUSR else '-',
        'w' if mode & stat.S_IWUSR else '-',
        'x' if mode & stat.S_IXUSR else '-',
        'r' if mode & stat.S_IRGRP else '-',
        'w' if mode & stat.S_IWGRP else '-',
        'x' if mode & stat.S_IXGRP else '-',
        'r' if mode & stat.S_IROTH else '-',
        'w' if mode & stat.S_IWOTH else '-',
        'x' if mode & stat.S_IXOTH else '-'
    ]
    return type + ''.join(permissions)
