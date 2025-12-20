from abc import ABC, abstractmethod

from src.core.config import BashConfig
from src.core.errors import BashNoSupportForLongFlagsError, BashInvalidFlagError, BashMoreParamsThenExpectedError, \
    BashError
from src.utils.immutable_dict import ImmutableDict


class BashCommand(ABC):
    _all_commands: dict[str, BashCommand] = {}

    def __init__(self, raw_params: list[str]):
        self._raw_params = raw_params
        self._flags: set[str] = set()
        self._params: list[str] = []

    @classmethod
    def _name(cls) -> str:
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
        self._flags, self._params = self._parse_raw_params(self._raw_params)
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
                        if not BashConfig.ignore_extra_flags:
                            raise BashInvalidFlagError
                    else:
                        flags.add(f)
            else:
                #                           +1 cuz we haven't append new parameter yet
                if (not self._max_params_count) or (len(params) + 1) <= self._max_params_count:
                    params.append(par)
                else:
                    raise BashMoreParamsThenExpectedError(self._name())
        return flags, params

    @classmethod
    def get_all_commands(cls) -> ImmutableDict[str, BashCommand]:
        return ImmutableDict(cls._all_commands)

    @classmethod
    def get_command(cls, key: str):
        return cls._all_commands[key]

    def __init_subclass__(cls: BashCommand, **kwargs):
        """Добавляем команды в словарь для автокомплита и вызова команд"""
        # LSBashCommand -> ls
        cls._all_commands[cls._name()] = cls
