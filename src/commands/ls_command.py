from src.terminal.command import BashCommand
from src.terminal.fs import FS


class LSBashCommand(BashCommand):
    @property
    def _supported_flags(self) -> str:
        return "la"

    @property
    def _max_params_count(self) -> int | None:
        return None

    def _exec(self):
       for param in self._params:
            if len(self._params) > 1:
                print(f"{param}:")
            self._print_items(param)

    def _print_items(self, dir_str: str):
        dir_path = FS.resolve_path(dir_str)
        is_dir = dir_path.is_dir()

        content = FS.ls(dir_str) if is_dir else [dir_path]
        show_hidden = 'a' in self._flags
        detailed = 'l' in self._flags
        print(content)

    def _validate_params(self):
        if not self._params:
            self._params.append(FS.cwd_str())
        else:
            for index, path in enumerate(self._params):

                if not FS.existing_path(path):
                    self._params.pop(index)
