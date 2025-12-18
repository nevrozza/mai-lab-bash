import pathlib

from src.terminal.command import BashCommand
from src.terminal.file_system.fs import fs
from src.terminal.file_system.resolve_path import resolve_path_deco
from src.terminal.file_system.utils import PathDetails
from src.utils.paths_grid_print import paths_grid_print


class LSBashCommand(BashCommand):
    @property
    def _supported_flags(self) -> str:
        return "la"

    def _exec(self):
        for param in self._params:
            if len(self._params) > 1:
                print(f"{param}:")
            # noinspection PyTypeChecker
            self._print_items(param)

    @resolve_path_deco
    def _print_items(self, path: pathlib.Path):
        show_hidden = 'a' in self._flags
        detailed = 'l' in self._flags
        is_dir = fs.properties.is_dir(path)
        content = list(
            filter(lambda p: show_hidden or not fs.properties.is_hidden(p), fs.ls(path) if is_dir else [path]))
        if detailed:
            self._detailed_print(is_dir, content)
        else:
            paths_grid_print(content)

    @staticmethod
    def _detailed_print(is_dir: bool, paths: list[pathlib.Path]):
        total_blocks = 0
        output_details: list[PathDetails] = []

        for path in paths:
            details = fs.properties.get_path_details(path)
            output_details.append(details)
            total_blocks += details.blocks
        is_dir and print(f"total {total_blocks}")

        for details in output_details:
            print(
                f"{details.permissions} {details.blocks:>2} {details.owner:<8} {details.group:<8} {details.size:>8}"
                f" {details.modification_time} {fs.normalize_name(details.name, path=details.path)}")

    def _validate_params(self):
        if not self._params:
            self._params.append(fs.cwd_str())
        else:
            for index, path in enumerate(self._params):
                if not fs.properties.existing_path(path):
                    self._params.pop(index)
