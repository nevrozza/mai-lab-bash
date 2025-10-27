import os
import pathlib
import stat
from functools import wraps


class FS:
    from_tilda = False

    @staticmethod
    def __fs_resolve_path(func):
        """
        internal Декоратор, который автоматически преобразует строковые пути в Path через FS.resolve_path()
        """

        @wraps(func)
        def wrapper(cls, path: str | pathlib.Path, *args, **kwargs):
            resolved_path = cls.resolve_path(path)
            return func(cls, resolved_path, *args, **kwargs)

        return wrapper

    @classmethod
    def cd(cls, path_str: str):
        cls.from_tilda = path_str.startswith('~')
        os.chdir(cls.resolve_path(path_str))

    @classmethod
    @__fs_resolve_path
    def ls(cls, path) -> list[pathlib.Path]:
        path = cls.resolve_path(path)
        return list(path.iterdir())

    @classmethod
    def cwd_str(cls) -> str:
        cwd = str(pathlib.Path.cwd())
        if cls.from_tilda:
            cwd = cwd.replace(str(pathlib.Path.home()), "~")
        return cwd

    @classmethod
    @__fs_resolve_path
    def existing_path(cls, path) -> pathlib.Path | None:
        if path.exists():
            return path
        else:
            return None

    @classmethod
    @__fs_resolve_path
    def is_hidden(cls, path) -> bool:
        if path.name.startswith("."):
            return True

        info = os.stat(path)
        if hasattr(info, "st_file_attributes"):
            return bool(info.st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN)  # TODO: check on windows!!
        else:
            return False

    @classmethod
    def normalize_name(cls, name: str) -> str:
        parts = name.split()
        if len(parts) > 1:
            return f"'{name}'"
        else:
            return name

    @classmethod
    def resolve_path(cls, path: str | pathlib.Path) -> pathlib.Path:
        return pathlib.Path(path).expanduser().resolve() if isinstance(path, str) else path
