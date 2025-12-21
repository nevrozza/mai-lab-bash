import pathlib

from src.core.errors import BashError, BashNoSuchFileOrDirectoryError, BashCommandError
from src.terminal.command import BashCommand
from src.terminal.file_system.fs import fs
from src.terminal.file_system.resolve_path import resolve_path_deco
from src.utils.print_builder import PrintBuilder
from src.utils.validate_params import default_validate_params


class CatBashCommand(BashCommand):
    """
    Вывод содержимого одного или нескольких файлов

    Директории игнорируются: выводится предупреждение
    """

    def _exec(self) -> tuple[list[BashError], str | None] | None:
        """Читает и объединяет содержимое всех указанных файлов"""
        print_builder = PrintBuilder()
        for path in self._params:
            # noinspection PyTypeChecker
            print_builder.append(self.read_file(path).strip())
        return [], print_builder.get()

    @staticmethod
    @resolve_path_deco
    def read_file(path: pathlib.Path) -> str:
        return path.read_text(encoding="utf-8", errors='ignore')  # hm...

    def _validate_params(self) -> list[BashError]:
        """Проверяет, что каждый путь существует и не является директорией"""
        def validate_path(path: str):
            if not fs.properties.existing_path(path):
                self._params.remove(path)
                return BashNoSuchFileOrDirectoryError(name=self.name(),
                                                      filename=path)
            elif fs.properties.is_dir(path):
                self._params.remove(path)
                return BashCommandError(name=self.name(), msg=f"'{path}': Is a directory")
            return None

        return default_validate_params(params=self._params, if_no_params=None, validate_path=validate_path)
