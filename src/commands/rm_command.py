import pathlib

from src.core.errors import BashError, BashCommandError, BashNoSuchFileOrDirectoryError
from src.terminal.command import UndoableBashCommand
from src.terminal.file_system.fs import fs
from src.terminal.file_system.resolve_path import resolve_path
from src.terminal.history import HistoryLine
from src.utils.validate_params import cp_mv_validate_params, default_validate_params


class RMBashCommand(UndoableBashCommand):
    @property
    def _supported_flags(self) -> str:
        return "rf"

    @classmethod
    def undo(cls, history_line: HistoryLine):
        flags, params = cls._parse_history_line(history_line)

        # def delete(t_d: pathlib.Path):
        #     fs.properties.existing_path(t_d) and fs.rm(t_d)
        #
        # for path in params[:-1]:
        #     if not fs.properties.existing_path(path):
        #         raise BashCommandError(name=cls.name(), msg="can't undo `cp`: original doesn't exist")
        #
        # if len(params) == 2:
        #     to_delete = resolve_path(params[1], history_line.wd)
        #     to_delete = (to_delete / resolve_path(params[0]).name) if fs.properties.is_dir(to_delete) else to_delete
        #     delete(to_delete)
        # else:
        #     for path in params[:-1]:
        #         delete_dir = resolve_path(params[-1], history_line.wd)
        #         to_delete = resolve_path(path, delete_dir)
        #         delete(to_delete)

    def _exec(self) -> tuple[list[BashError], str | None] | None:
        for path in self._params:
            to_rm = resolve_path(path)
            trash_folder = resolve_path(".trash")
            if fs.properties.is_dir(to_rm):
                if "f" not in self._flags:
                    answer = input(f"rm dir '{to_rm}'? [y/n] ")
                    if answer != "y":
                        continue
                trash_folder /= to_rm.name
            fs.mv(to_rm, trash_folder)

    def _validate_params(self) -> list[BashError]:
        def validate_path(path: str):
            if not fs.properties.existing_path(path):
                self._params.remove(path)
                return BashNoSuchFileOrDirectoryError(name=self.name(),
                                                      filename=path)
            elif fs.properties.is_dir(path) and "r" not in self._flags:
                raise BashCommandError(self.name(), msg=f"can't rm: '{path}' is a dir but '-r' not specified")
            return None

        return default_validate_params(
            params=self._params,
            if_no_params=None,
            validate_path=validate_path
        )
