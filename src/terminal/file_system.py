import os
import pathlib


class FileSystem:
    def __init__(self):
        self.from_tilda = False

    def cd(self, path_str: str):
        if path_str.startswith('~'):
            self.from_tilda = True
        os.chdir(pathlib.Path(path_str).expanduser())

    def cwd_str(self) -> str:
        cwd = str(pathlib.Path.cwd())
        if self.from_tilda:
            cwd = cwd.replace(str(pathlib.Path.home()), "~")
        return cwd
