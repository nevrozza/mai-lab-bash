import shutil

from src.core.errors import BashError
from src.terminal.command import BashCommand
from src.terminal.file_system.resolve_path import resolve_path
from src.utils.validate_params import cp_mv_validate_params


class CPBashCommand(BashCommand):
    def _exec(self) -> str:
        if len(self._params) == 2:
            shutil.copy2(resolve_path(self._params[0]), resolve_path(self._params[1]))
        else:
            for path in self._params[:-1]:
                shutil.copy2(resolve_path(path), resolve_path(self._params[-1]))
        return ""

    def _validate_params(self) -> list[BashError]:
        return cp_mv_validate_params(params=self._params, command_name=self.name())
