from src.core.errors import BashError, BashNoSuchFileOrDirectory, BashNotADirectory
from src.terminal.command import BashCommand
from src.terminal.file_system.fs import fs


class CDBashCommand(BashCommand):
    @property
    def _max_params_count(self) -> int:
        return 1

    def _exec(self) -> str:
        len(self._params) == 1 and fs.cd(self._params[0])
        return ""

    def _validate_params(self) -> list[BashError]:
        # Здесь все ошибки являются критическими, поэтому raise

        if not self._params:
            return []

        # We know: there is only one parameter
        path = self._params[0]
        command_name = self._name()
        if not fs.properties.existing_path(path):
            raise BashNoSuchFileOrDirectory(name=command_name, filename=path)
        elif not fs.properties.is_dir(path):
            raise BashNotADirectory(name=command_name, filename=path)

        return []
