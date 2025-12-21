import os
import pathlib
import shutil
from shutil import rmtree

from src.terminal.file_system.fs_properties import FSProperties
from src.terminal.file_system.resolve_path import resolve_path, resolve_path_deco
from src.utils.quoting_type import QuotingType


def create_fs():
    """Factory для FS"""
    # Потом можно будет добавить имплементацию для Windows (прокидывать другой FS)
    return FS(FSProperties())


class FS:
    """Обёртка для операций с файловой системой"""

    def __init__(self, properties: FSProperties):
        self.from_tilda = False
        self.properties = properties

    def cp(self, path: pathlib.Path, destination: pathlib.Path):
        """Поддерживает файл и директорию"""
        if not self.properties.is_dir(path):
            shutil.copy2(path, destination)
        else:
            shutil.copytree(path, destination / path.name, dirs_exist_ok=True)

    @staticmethod
    def mv(path: pathlib.Path, destination: pathlib.Path):
        """Поддерживает файл и директорию"""
        shutil.move(path, destination)

    @resolve_path_deco
    def rm(self, path: pathlib.Path):
        """Поддерживает файл и директорию"""
        if self.properties.is_dir(path):
            rmtree(path, ignore_errors=True)
        else:
            os.remove(path)

    def cd(self, path_str: str):
        """
        Меняет текущую рабочую директорию

        Если путь абсолютный - учитывает, использовалась ли тильда: `влияет на` ``cwd_str``
        """
        if path_str and path_str[0] in ("~", "/"):
            self.from_tilda = path_str.startswith("~")
        os.chdir(resolve_path(path_str))

    @resolve_path_deco
    def ls(self, path) -> list[pathlib.Path]:
        """:return: Отсортированный список содержимого директории."""
        return list(sorted(path.iterdir()))

    def cwd_str(self) -> str:
        """:return: Строковой путь текущей директории, заменяя домашнюю на ~ при необходимости."""
        cwd = str(pathlib.Path.cwd())
        if self.from_tilda:
            cwd = cwd.replace(str(pathlib.Path.home()), "~")
        return cwd

    @staticmethod
    def normalize_name(name: str, quoting_type: QuotingType = QuotingType.ESCAPING_TYPE,
                       path: pathlib.Path | None = None) -> str:
        """Форматирует имя файла для вывода: экранирует пробелы или оборачивает в кавычки"""
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

        quoted: str = quoted_name()
        if path and fs.properties.is_dir(path):  # Add '/' if it's folder
            quoted += "/"

        return quoted


fs = create_fs()
