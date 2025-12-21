import inspect
import shlex
from abc import ABC

from src.core.errors import BashError
from src.terminal.command import BashCommand
from src.terminal.history import HistoryLine


class UndoableBashCommand(BashCommand, ABC):
    undoable_commands: set[str] = set()

    @classmethod
    def _parse_history_line(cls, history_line: HistoryLine) -> tuple[set[str], list[str]]:
        flags: set[str] = set()
        params = []
        for par in shlex.split(history_line.command_line)[1:]:
            if par.startswith("-") and len(par) > 1:
                for f in par[1:]:
                    flags.add(f)
            else:
                params.append(par)
        return flags, params

    @classmethod
    def undo(cls, history_line: HistoryLine) -> list[BashError]:
        pass

    def __init_subclass__(cls: UndoableBashCommand, **kwargs):
        """Добавляем команды в словарь для автокомплита и вызова команд"""
        super().__init_subclass__(**kwargs)
        if not inspect.isabstract(cls):
            cls.undoable_commands.add(cls.name())  # для поиска в undo
