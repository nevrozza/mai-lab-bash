import inspect
import shlex
from abc import ABC, abstractmethod

from src.core.errors import BashError
from src.terminal.command import BashCommand
from src.terminal.history import HistoryLine


class UndoableBashCommand(BashCommand, ABC):
    """Родительский класс для команд, поддерживающих отмену (``undo``)"""

    undoable_commands: set[str] = set()

    @classmethod
    @abstractmethod
    def undo(cls, history_line: HistoryLine) -> list[BashError]:
        """Отмена команды"""
        pass

    @classmethod
    def _parse_history_line(cls, history_line: HistoryLine) -> tuple[set[str], list[str]]:
        """
        Извлекает флаги и параметры из сохранённой строки команды

        Отличие: мы знаем, что строка выполнилась без ошибок
        """
        flags: set[str] = set()
        params = []
        for par in shlex.split(history_line.command_line)[1:]:
            if par.startswith("-") and len(par) > 1:
                for f in par[1:]:
                    flags.add(f)
            else:
                params.append(par)
        return flags, params

    def __init_subclass__(cls, **kwargs):
        """Добавляем команды в словарь для автокомплита и вызова команд"""
        super().__init_subclass__(**kwargs)
        if not inspect.isabstract(cls):
            cls.undoable_commands.add(cls.name())  # для поиска в undo
