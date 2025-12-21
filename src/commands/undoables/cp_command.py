import pathlib

from src.commands.custom_abc.undoable_command import UndoableBashCommand
from src.core.errors import BashError, BashCommandError
from src.terminal.file_system.fs import fs
from src.terminal.file_system.resolve_path import resolve_path
from src.terminal.history import HistoryLine
from src.utils.validate_params import cp_mv_validate_params


class CPBashCommand(UndoableBashCommand):
    """
    Команда копирования файлов/директорий

    Поддерживает копию папок с содержимым и undo
    """

    @property
    def _supported_flags(self) -> str:
        return "r"

    @classmethod
    def undo(cls, history_line: HistoryLine):
        """Отменяет копирование: просто удаляет созданные копии."""
        flags, params = cls._parse_history_line(history_line)

        def delete(t_d: pathlib.Path):
            fs.properties.existing_path(t_d) and fs.rm(t_d)

        # Проверка существовния исходных файлов, т.к. иначе отмена бессмысленна (и невозможна в текущей реализации)
        for path in params[:-1]:
            if not fs.properties.existing_path(path):
                raise BashCommandError(name=cls.name(), msg="can't undo `cp`: original doesn't exist")

        if len(params) == 2:
            to_delete = resolve_path(params[1], history_line.wd)
            to_delete = (to_delete / resolve_path(params[0]).name) if fs.properties.is_dir(to_delete) else to_delete
            delete(to_delete)
        else:
            for path in params[:-1]:
                delete_dir = resolve_path(params[-1], history_line.wd)
                to_delete = resolve_path(path, delete_dir)
                delete(to_delete)

    def _exec(self) -> tuple[list[BashError], str | None] | None:
        for path in self._params[:-1]:
            fs.cp(resolve_path(path), resolve_path(self._params[-1]))
        return None

    def _validate_params(self) -> list[BashError]:
        """Проверяет аргументы с учётом флага ``-r`` для директорий"""
        return cp_mv_validate_params(params=self._params, command_name=self.name(), allow_dirs="r" in self._flags)
