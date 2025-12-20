import inspect
import shlex
from abc import ABC, abstractmethod

from src.core.config import BashConfig
from src.core.errors import BashNoSupportForLongFlagsError, BashInvalidFlagError, BashMoreParamsThenExpectedError, \
    BashError
from src.terminal.history import HistoryLine
from src.utils.immutable_dict import ImmutableDict


class BashCommand(ABC):
    _all_commands: dict[str, BashCommand] = {}

    def __init__(self, raw_params: list[str], command_line: str):
        self.__raw_params = raw_params
        self._flags: set[str] = set()
        self._params: list[str] = []
        self.command_line = command_line

    @classmethod
    def name(cls) -> str:
        # override for custom naming
        return cls.__name__.removesuffix("BashCommand").lower()

    @property
    def _supported_flags(self) -> str:
        return ""

    @property
    def _max_params_count(self) -> int | None:
        return None

    @abstractmethod
    def _exec(self) -> str:
        pass

    @abstractmethod
    def _validate_params(self) -> list[BashError]:
        pass

    def execute(self) -> tuple[list[BashError], str]:
        self._flags, self._params = self._parse_raw_params(self.__raw_params)
        return self._validate_params(), self._exec()

    def _parse_raw_params(self, raw_params: list[str]) -> tuple[set[str], list[str]]:
        flags: set[str] = set()
        params = []
        for par in raw_params:
            if par.startswith("-") and len(par) > 1:
                if par.startswith("--"):
                    raise BashNoSupportForLongFlagsError
                for f in par[1:]:
                    if f not in self._supported_flags:
                        if not BashConfig.IGNORE_EXTRA_FLAGS:
                            raise BashInvalidFlagError(name=self.name(), flag=f, supported=self._supported_flags)
                    else:
                        flags.add(f)
            else:
                #                           +1 cuz we haven't append new parameter yet
                if (not self._max_params_count) or (len(params) + 1) <= self._max_params_count:
                    params.append(par)
                else:
                    raise BashMoreParamsThenExpectedError(self.name())
        return flags, params

    @classmethod
    def get_all_commands(cls) -> ImmutableDict[str, BashCommand]:
        return ImmutableDict(cls._all_commands)

    @classmethod
    def get_command(cls, key: str):
        return cls._all_commands[key]

    def __init_subclass__(cls: BashCommand, **kwargs):
        """Добавляем команды в словарь для автокомплита и вызова команд"""

        if not inspect.isabstract(cls):
            cls._all_commands[cls.name()] = cls


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
    def undo(cls, history_line: HistoryLine):
        pass

    def __init_subclass__(cls: UndoableBashCommand, **kwargs):
        """Добавляем команды в словарь для автокомплита и вызова команд"""
        super().__init_subclass__(**kwargs)
        if not inspect.isabstract(cls):
            cls.undoable_commands.add(cls.name())  # для поискаhgi undo
