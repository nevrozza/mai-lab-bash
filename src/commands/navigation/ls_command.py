import pathlib

from src.core.errors import BashError, BashNoSuchFileOrDirectoryError
from src.terminal.command import BashCommand
from src.terminal.file_system.fs import fs
from src.terminal.file_system.resolve_path import resolve_path_deco
from src.terminal.file_system.utils import PathDetails
from src.utils.paths_grid_print import paths_grid_output
from src.utils.print_builder import PrintBuilder
from src.utils.validate_params import default_validate_params


class LSBashCommand(BashCommand):
    """
    Команда просмотра содержимого директории

    Поддерживает флаги ``-l`` и ``-a``
    """

    @property
    def _supported_flags(self) -> str:
        return "la"

    def _exec(self) -> tuple[list[BashError], str | None] | None:
        print_builder = PrintBuilder()
        for path in self._params:
            if len(self._params) > 1:
                fs.properties.is_dir(path) and print_builder.append(f"{path}:")
            # noinspection PyTypeChecker
            print_builder.append(self._get_output_items(path))
        return [], print_builder.get()

    @resolve_path_deco
    def _get_output_items(self, path: pathlib.Path) -> PrintBuilder:
        """Возвращает отформатированный вывод для одного пути"""
        show_hidden = 'a' in self._flags
        detailed = 'l' in self._flags
        is_dir = fs.properties.is_dir(path)
        content = list(
            filter(lambda p: show_hidden or not fs.properties.is_hidden(p), fs.ls(path) if is_dir else [path]))
        if detailed:
            return self._detailed_output(is_dir, content)
        else:
            return paths_grid_output(content)

    @staticmethod
    def _detailed_output(is_dir: bool, paths: list[pathlib.Path]) -> PrintBuilder:
        """Формирует подробный вывод (-l)"""
        builder = PrintBuilder()
        total_blocks = 0
        output_details: list[PathDetails] = []

        for path in paths:
            details = fs.properties.get_path_details(path)
            output_details.append(details)
            total_blocks += details.blocks
        is_dir and builder.append(f"total {total_blocks}")

        for details in output_details:
            builder.append(
                f"{details.permissions} {details.blocks:>2} {details.owner:<8} {details.group:<8} {details.size:>8}"
                f" {details.modification_time} {fs.normalize_name(details.name, path=details.path)}")
        return builder

    def _validate_params(self) -> list[BashError]:
        """
        Проверяет существование путей

        если параметров нет – использует текущую директорию
        если в путях ошибка – логгирование и пропуск текущего пути
        """
        def validate_path(path: str):
            if not fs.properties.existing_path(path):
                self._params.remove(path)
                return BashNoSuchFileOrDirectoryError(name=self.name(),
                                                      filename=path)
            return None

        return default_validate_params(
            params=self._params,
            if_no_params=lambda: self._params.append(fs.cwd_str()),
            validate_path=validate_path
        )
