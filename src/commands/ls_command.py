import pathlib

from src.terminal.command import BashCommand
from src.terminal.file_system.fs import fs
from src.terminal.file_system.resolve_path import resolve_path_deco
from src.utils.files_grid_print import files_grid_print


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
        content = list(filter(lambda p: show_hidden or not fs.properties.is_hidden(p), fs.ls(path) if is_dir else [path]))
        if detailed:
            ...
        else:
            files_grid_print(content)

    def _validate_params(self):
        if not self._params:
            self._params.append(fs.cwd_str())
        else:
            for index, path in enumerate(self._params):
                if not fs.properties.existing_path(path):
                    self._params.pop(index)
