import importlib
from pathlib import Path


def import_default_commands():
    """Импортирует все (дефолтные) команды из папки commands"""
    commands_dir = Path(__file__).parent
    if not commands_dir.exists():
        raise ImportError("import_all_commands: Папка с командами указана неверно")
    for file_path in commands_dir.glob("*_command.py"):
        module_name = f"src.commands.{file_path.stem}"
        importlib.import_module(module_name)