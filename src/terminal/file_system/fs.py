import os
import pathlib

from src.terminal.file_system.fs_properties import FSProperties
from src.terminal.file_system.resolve_path import resolve_path, resolve_path_deco
from src.utils.quoting_type import QuotingType


def create_fs():  # Потом можно будет добавить имплементацию для Windows (прокидывать другой FS)
    return FS(FSProperties())


class FS:
    def __init__(self, properties: FSProperties):
        self.from_tilda = False
        self.properties = properties

    def cd(self, path_str: str):
        if path_str and path_str[0] in ("~", "/"):
            self.from_tilda = path_str.startswith("~")
        os.chdir(resolve_path(path_str))

    @resolve_path_deco
    def ls(self, path) -> list[pathlib.Path]:
        return list(sorted(path.iterdir()))

    def cwd_str(self) -> str:
        cwd = str(pathlib.Path.cwd())
        if self.from_tilda:
            cwd = cwd.replace(str(pathlib.Path.home()), "~")
        return cwd

    @staticmethod
    def normalize_name(name: str, quoting_type: QuotingType = QuotingType.ESCAPING_TYPE,
                       path: pathlib.Path | None = None) -> str:
        parts = name.split()

        def quoted_name():
            if len(parts) > 1:
                if quoting_type != QuotingType.ESCAPING_TYPE:
                    quote = quoting_type.value
                    return f"{quote}{name}{quote}"
                else:  # QuotingType.ESCAPING_TYPE
                    return "\\ ".join(parts)
            else:
                return name

        quoted_name = quoted_name()
        if path and fs.properties.is_dir(path):  # Add '/' if it's folder
            quoted_name += "/"

        return quoted_name


fs = create_fs()
