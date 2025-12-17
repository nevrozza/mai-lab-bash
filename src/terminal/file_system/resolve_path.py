import pathlib
from functools import wraps


def resolve_path_deco(func):
    """
    internal для FS Декоратор, который автоматически преобразует строковые пути в Path через FS.resolve_path()
    """

    @wraps(func)
    def wrapper(path: str | pathlib.Path, *args, **kwargs):
        resolved_path = resolve_path(path)
        # print(path, resolved_path.exists())
        return func(resolved_path, *args, **kwargs)

    return wrapper


# Not in FS because of using in FS and FSProperties
def resolve_path(path: str | pathlib.Path) -> pathlib.Path:
                            # forced space escaping for tab-tab-tab folder completion
    return pathlib.Path(path.replace(r"\ ", " ")).expanduser().resolve() if isinstance(path, str) else path
