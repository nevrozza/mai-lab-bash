import os
import pathlib


class FileSystem:
    def __init__(self):
        self.from_home = True

    def cd(self, path: pathlib.Path):
        os.chdir(path)

    def cwd_str(self) -> str:
        cwd = str(pathlib.Path.cwd())
        if self.from_home:
            cwd = cwd.replace(str(pathlib.Path.cwd()), "~")
        return cwd
