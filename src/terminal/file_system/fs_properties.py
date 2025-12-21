import os
import pathlib
import pwd
import stat
import time

import grp

from src.terminal.file_system.resolve_path import resolve_path_deco
from src.terminal.file_system.utils import PathDetails, get_permission_string


class FSProperties:
    """Утилиты для проверки свойств файлов и директорий"""

    @staticmethod
    @resolve_path_deco
    def get_path_details(path: pathlib.Path) -> PathDetails:
        """:return: Расширенная информация о файле или директории"""

        # Windows?
        stat = path.stat()
        blocks = stat.st_blocks
        size = stat.st_size

        owner = pwd.getpwuid(stat.st_uid).pw_name
        group = grp.getgrgid(stat.st_gid).gr_name

        modification_time_float = stat.st_mtime
        modification_time = time.strftime('%b %d %H:%M', time.localtime(modification_time_float))

        return PathDetails(
            permissions=get_permission_string(path),
            blocks=blocks,
            owner=owner,
            group=group,
            size=size,
            modification_time=modification_time,
            name=path.name,
            path=path
        )

    @staticmethod
    @resolve_path_deco
    def existing_path(path) -> pathlib.Path | None:
        """Проверяет существование пути
        :return: Path или None."""
        if path.exists():
            return path
        else:
            return None

    @staticmethod
    @resolve_path_deco
    def is_hidden(path) -> bool:
        if path.name.startswith("."):
            return True

        info = os.stat(path)
        if hasattr(info, "st_file_attributes"): # TODO: check on windows!!
            # getattr because of pre-commit =/
            info = path.stat()
            attrs = getattr(info, "st_file_attributes", 0)
            hidden_flag = getattr(stat, "FILE_ATTRIBUTE_HIDDEN", 0)
            return bool(attrs & hidden_flag)
        else:
            return False

    @staticmethod
    @resolve_path_deco
    def is_dir(path):
        return path.is_dir()
