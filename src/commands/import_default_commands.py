import importlib
from pathlib import Path


def import_default_commands():
    """Импортирует все (дефолтные) команды из папки commands"""
    commands_dir = Path(__file__).parent
    if not commands_dir.exists():
        raise ImportError("import_all_commands: Папка с командами указана неверно")
    for file_path in commands_dir.rglob("*_command.py"):
        module_name = f"src.commands.{str(file_path).split("commands/")[-1].replace("/", ".").removesuffix(".py")}"
        importlib.import_module(module_name)