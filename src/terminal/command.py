import inspect
from abc import ABC, abstractmethod

from src.core.config import BashConfig
from src.core.errors import BashNoSupportForLongFlagsError, BashInvalidFlagError, BashMoreParamsThenExpectedError, \
    BashError
from src.utils.immutable_dict import ImmutableDict


class BashCommand(ABC):
    """Родительский класс для всех команд терминала."""
    _all_commands: dict[str, type[BashCommand]] = {}

    def __init__(self, raw_params: list[str], command_line: str):
        self.__raw_params = raw_params
        self._flags: set[str] = set()
        self._params: list[str] = []
        self.command_line = command_line

    @classmethod
    def name(cls) -> str:
        """
        Возвращает имя команды

        По умолчанию – имя класса без суффикса
        """
        # override for custom naming
        return cls.__name__.removesuffix("BashCommand").lower()

    @property
    def _supported_flags(self) -> str:
        """
        Строка поддерживаемых флагов

        Пример: 'ri' для -r и -i
        """
        return ""

    @property
    def _max_params_count(self) -> int | None:
        """Максимальное число параметров (None – без ограничения)"""
        return None

    @abstractmethod
    def _exec(self) -> tuple[list[BashError], str | None] | None:
        """Внутренняя логика выполнения команды"""
        pass

    @abstractmethod
    def _validate_params(self) -> list[BashError]:
        """Внутренняя валидация параметров команды"""
        pass

    def execute(self) -> tuple[list[BashError], tuple[list[BashError], str | None]]:
        """
        Ручка для запуска команды: парсит параметры, валидирует ``_validate_params`` и запускает команду ``_exec``

        :return: `tuple[list[BashError], tuple[list[BashError], str]]` – (список ошибок во время валидации, (во время выполнения, вывод))
        """
        self._flags, self._params = self._parse_raw_params(self.__raw_params)
        return self._validate_params() or [], self._exec() or ([], None)

    def _parse_raw_params(self, raw_params: list[str]) -> tuple[set[str], list[str]]:
        """
        Парсит параметры: отделяет флаги, проверяет на кол-во параметров

        :return: `tuple[set[str], list[str]]` - (мн-во флагов, список параметров)
        """
        flags: set[str] = set()
        params: list[str] = []
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
    def get_all_commands(cls) -> ImmutableDict[str, type[BashCommand]]:
        """
        Возвращает неизменяемый словарь **всех** зарегистрированных команд

        Используется для автокомплита и поиска команд по их названию
        """
        return ImmutableDict(cls._all_commands)

    @classmethod
    def get_command(cls, key: str) -> type[BashCommand]:
        return cls._all_commands[key]

    def __init_subclass__(cls, **kwargs):
        """Добавляем команды в словарь для автокомплита и вызова команд"""

        # Не добавляем абстракции (UndoableBashCommand, ArchiveBashCommand, UnarchiveBashCommand)
        if not inspect.isabstract(cls):
            cls._all_commands[cls.name()] = cls
