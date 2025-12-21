import pathlib

from src.commands.custom_abc.undoable_command import UndoableBashCommand
from src.core.errors import BashError, BashCommandError
from src.terminal.file_system.fs import fs
from src.terminal.file_system.resolve_path import resolve_path
from src.terminal.history import HistoryLine
from src.utils.validate_params import cp_mv_validate_params


class MVBashCommand(UndoableBashCommand):
    """
    Команда перемещения файлов/директорий

    Поддерживает отмену
    """

    @classmethod
    def undo(cls, history_line: HistoryLine) -> list[BashError]:
        errors: list[BashError] = []
        flags, params = cls._parse_history_line(history_line)

        def move(path: pathlib.Path, dest: pathlib.Path):
            if fs.properties.existing_path(path):
                fs.mv(path, dest)
            else:
                errors.append(BashCommandError(name=cls.name(), msg="can't undo `mv`: file/dir doesn't exist"))

        if len(params) == 2:
            src = resolve_path(params[0], history_line.wd)
            dst = resolve_path(params[1], history_line.wd)

            if fs.properties.is_dir(dst):
                moved_path = dst / src.name
            else:
                moved_path = dst
            move(moved_path, src)

        else:
            dst_dir = resolve_path(params[-1], history_line.wd)
            for src_param in params[:-1]:
                src = resolve_path(src_param, history_line.wd)
                moved_path = dst_dir / src.name
                move(moved_path, src)
        return errors

    def _exec(self) -> tuple[list[BashError], str | None] | None:
        """Выполняет перемещение указанных путей в целевую директорию или под новым именем"""
        errors: list[BashError] = []
        dist_path = resolve_path(self._params[-1])
        for path in self._params[:-1]:
            p1 = resolve_path(path)
            if not fs.properties.existing_path(dist_path / p1.name):
                if fs.properties.is_dir(p1):
                    dist_path /= p1.name
                fs.mv(p1, dist_path)
            else:
                errors.append(BashCommandError(name=self.name(), msg=f"destination '{dist_path}' already exists"))
        return errors, ""

    def _validate_params(self) -> list[BashError]:
        return cp_mv_validate_params(params=self._params, command_name=self.name(), allow_dirs=True)
