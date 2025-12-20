import shutil

from src.core.errors import BashError
from src.terminal.command import UndoableBashCommand
from src.terminal.file_system.fs import fs
from src.terminal.file_system.resolve_path import resolve_path
from src.terminal.history import HistoryLine
from src.utils.validate_params import cp_mv_validate_params


class CPBashCommand(UndoableBashCommand):
    @classmethod
    def undo(cls, history_line: HistoryLine):
        flags, params = cls._parse_history_line(history_line)
        if len(params) == 2:
            to_delete = resolve_path(params[1], history_line.wd)
            fs.rm(to_delete)
        else:
            for path in params[:-1]:
                delete_dir = resolve_path(params[-1], history_line.wd)
                to_delete = resolve_path(path, delete_dir)
                fs.rm(to_delete)

    def _exec(self) -> str | None:
        if len(self._params) == 2:
            shutil.copy2(resolve_path(self._params[0]), resolve_path(self._params[1]))
        else:
            for path in self._params[:-1]:
                shutil.copy2(resolve_path(path), resolve_path(self._params[-1]))

    def _validate_params(self) -> list[BashError]:
        return cp_mv_validate_params(params=self._params, command_name=self.name())
