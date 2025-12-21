import importlib
from pathlib import Path


def import_default_commands():
    """Импортирует все `дефолтные` команды из папки commands"""
    commands_dir = Path(__file__).parent
    # Находим src' для импортов: `src.commands.archive.tar_command`
    src_dir = commands_dir
    #                               Чтобы не было бесконечного цикла
    while src_dir.name != "src" and src_dir.parent != src_dir:
        src_dir = src_dir.parent
    if src_dir.name != "src":
        raise ImportError("Не удалось найти корневую папку 'src'")

    for file_path in commands_dir.rglob("*_command.py"):
        # Получаем путь относительно src/
        relative_to_src = file_path.relative_to(src_dir.parent)
        module_name = str(relative_to_src).replace("/", ".").removesuffix(".py")
        importlib.import_module(module_name)
