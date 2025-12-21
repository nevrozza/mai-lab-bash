from src.commands.custom_abc.undoable_command import UndoableBashCommand
from src.core.errors import BashError, BashCommandError, BashNoSuchFileOrDirectoryError

from src.terminal.file_system.fs import fs
from src.terminal.file_system.resolve_path import resolve_path
from src.terminal.history import HistoryLine
from src.utils.validate_params import default_validate_params


class RMBashCommand(UndoableBashCommand):
    """
    Команда удаления файлов/директорий с перемещением в ``.trash``

    Поддерживает ``undo``
    """

    @property
    def _supported_flags(self) -> str:
        return "rf"

    @classmethod
    def undo(cls, history_line: HistoryLine):
        """Восстанавливает удалённые файлы из ``.trash`` в исходное расположение"""
        flags, params = cls._parse_history_line(history_line)
        trash_dir = resolve_path(".trash", history_line.wd)

        for param in params:
            original_path = resolve_path(param, history_line.wd)
            trash_path = trash_dir / original_path.name

            if not fs.properties.existing_path(trash_path):
                raise BashCommandError(
                    name=cls.name(),
                    msg=f"can't undo `rm`: '{trash_path}' not found in .trash"
                )
            fs.mv(trash_path, original_path)

    def _exec(self) -> tuple[list[BashError], str | None] | None:
        """
        Выполняет удаление: перемещает файлы/директории в ``.trash``

        Если нет флага ``f`` при удалении директории, потребуется подтверждение
        """

        for path in self._params:
            to_rm = resolve_path(path)
            trash_folder = resolve_path(".trash")
            trash_folder.mkdir(parents=True, exist_ok=True)
            if fs.properties.is_dir(to_rm):

                # Подтверждение удаления директории без флага -f
                if "f" not in self._flags:
                    answer = input(f"rm dir '{to_rm}'? [y/n] ")
                    if answer != "y":
                        continue

                trash_folder /= to_rm.name
            fs.mv(to_rm, trash_folder)
        return None

    def _validate_params(self) -> list[BashError]:
        """Проверяет, что удаляемые пути существуют,
        не являются текущей/родительской директорией и соответствуют флагам (r for dir)"""
        def validate_path(path: str):
            if not fs.properties.existing_path(path):
                self._params.remove(path)
                return BashNoSuchFileOrDirectoryError(name=self.name(),
                                                      filename=path)
            elif fs.properties.is_dir(path) and "r" not in self._flags:
                raise BashCommandError(self.name(), msg=f"can't rm: '{path}' is a dir but '-r' not specified")

            resolved = resolve_path(path)
            cwd = resolve_path(fs.cwd_str())
            if resolved == cwd or resolved in cwd.parents:
                raise BashCommandError(self.name(), msg=f"cannot remove '{path}': it is current or parent directory")

            return None

        return default_validate_params(
            params=self._params,
            if_no_params=None,
            validate_path=validate_path
        )
