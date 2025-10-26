import os
import pathlib


class FS:
    from_tilda = False

    @classmethod
    def cd(cls, path_str: str):
        if path_str.startswith('~'):
            cls.from_tilda = True
        os.chdir(pathlib.Path(path_str).expanduser())

    @classmethod
    def cwd_str(cls) -> str:
        cwd = str(pathlib.Path.cwd())
        if cls.from_tilda:
            cwd = cwd.replace(str(pathlib.Path.home()), "~")
        return cwd
