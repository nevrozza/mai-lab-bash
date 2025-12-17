import os
import pathlib
import stat

from src.terminal.file_system.resolve_path import resolve_path_deco


class FSProperties:
    @staticmethod
    @resolve_path_deco
    def existing_path(path) -> pathlib.Path | None:
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
        if hasattr(info, "st_file_attributes"):
            return bool(info.st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN)  # TODO: check on windows!!
        else:
            return False

    @staticmethod
    @resolve_path_deco
    def is_dir(path):
        return path.is_dir()
