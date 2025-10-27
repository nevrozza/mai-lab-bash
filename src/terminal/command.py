import importlib
from abc import ABC, abstractmethod
from pathlib import Path

from src.utils.config import BashConfig
from src.utils.errors import BashNoSupportForLongFlagsError, BashInvalidFlagError, BashMoreParamsThenExpectedError
from src.utils.immutable_dict import ImmutableDict


class BashCommand(ABC):
    _all_commands: dict[str, 'BashCommand'] = {}

    @property
    @abstractmethod
    def _supported_flags(self) -> str:
        pass

    @property
    @abstractmethod
    def _max_params_count(self) -> int | None:
        pass

    @abstractmethod
    def _exec(self):
        pass

    @abstractmethod
    def _validate_params(self):
        pass

    def execute(self):
        self._flags, self._params = self._parse_raw_params(self._raw_params)
        self._validate_params()
        self._exec()

    def __init__(self, raw_params: list[str]):
        self._raw_params = raw_params
        self._flags: set[str] = set()
        self._params: list[str] = []

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
                if not self._max_params_count or len(params) <= self._max_params_count:
                    params.append(par)
                else:
                    raise BashMoreParamsThenExpectedError
        return flags, params

    @classmethod
    def get_all_commands(cls) -> ImmutableDict[str, 'BashCommand']:
        return ImmutableDict(cls._all_commands)

    @classmethod
    def get_command(cls, key: str):
        return cls._all_commands[key]

    def __init_subclass__(cls: 'BashCommand', **kwargs):
        """Добавляем команды в словарь для автокомплита и вызова команд"""
        # LSBashCommand -> ls
        cls._all_commands[cls.__name__.removesuffix("BashCommand").lower()] = cls

    @classmethod
    def import_all_commands(cls):
        if cls._all_commands:
            return

        """Импортирует все команды из папки commands"""
        commands_dir = Path(__file__).parent.parent / "commands"
        if not commands_dir.exists():
            raise ImportError("import_all_commands: Папка с командами указана неверно")
        for file_path in commands_dir.glob("*_command.py"):
            module_name = f"src.commands.{file_path.stem}"
            importlib.import_module(module_name)
