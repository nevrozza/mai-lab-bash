import importlib
from abc import ABC
from pathlib import Path

from src.utils.immutable_dict import ImmutableDict


class BashCommand(ABC):
    _all_commands: dict[str, 'BashCommand'] = {}

    @classmethod
    def get_all_commands(cls) -> ImmutableDict[str, 'BashCommand']:
        return ImmutableDict(cls._all_commands)

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
            raise ImportError("_load_commands: Папка с командами указана неверно")
        for file_path in commands_dir.glob("*_command.py"):
            module_name = f"src.commands.{file_path.stem}"
            importlib.import_module(module_name)
