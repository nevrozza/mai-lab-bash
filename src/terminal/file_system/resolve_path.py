import inspect
import pathlib
from functools import wraps


def resolve_path_deco(func):
    """
    Декоратор, который автоматически преобразует строковой путь в Path через resolve_path()

    Работает как для функций, так и для методов

    Путь обязательно должен быть первым параметром (после self, cls) или назван path
    """

    sig = inspect.signature(func)
    params = list(sig.parameters.keys())

    @wraps(func)
    def func_wrapper(path: str | pathlib.Path, *args, **kwargs):
        resolved_path = resolve_path(path)
        return func(path=resolved_path, *args, **kwargs)

    @wraps(func)
    def method_wrapper(cls_or_self, path: str | pathlib.Path, *args, **kwargs):
        resolved_path = resolve_path(path)
        return func(cls_or_self, path=resolved_path, *args, **kwargs)

    # Определяем, является ли функция методом (по наличию self/cls)
    if params and (params[0] == 'self' or params[0] == 'cls'):  # Сомнительно, но окей
        return method_wrapper
    else:
        return func_wrapper


# Not in FS because of using in FS and FSProperties
def resolve_path(path: str | pathlib.Path, wd: str | pathlib.Path | None = None) -> pathlib.Path:
    """
    Преобразует строковый путь в абсолютный pathlib.Path с поддержкой ~, относительных путей и экранированных пробелов

    :param path: путь (str | Path)
    :param wd: рабочая директория для разрешения относительных путей (работает только для относительного пути)
    :return: абсолютный pathlib.Path
    """
    a = pathlib.Path(
        ((str(wd) + "/") if (wd and not path.startswith(("~", "/"))) else "") +  # support custom wd
        # forced space escaping for tab-tab-tab folder completion (workaround)
        path.replace(r"\ ", " ")).expanduser().resolve() if isinstance(path, str) else path
    return a
