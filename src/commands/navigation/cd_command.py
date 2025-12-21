from src.core.errors import BashError, BashNoSuchFileOrDirectoryError, BashNotADirectoryError
from src.terminal.command import BashCommand
from src.terminal.file_system.fs import fs


class CDBashCommand(BashCommand):
    """Команда смены current working directory"""

    @property
    def _max_params_count(self) -> int:
        return 1

    def _exec(self) -> tuple[list[BashError], str | None] | None:
        """Меняет директорию, если указан путь, иначе – скип"""
        len(self._params) == 1 and fs.cd(self._params[0])
        return None

    def _validate_params(self) -> list[BashError]:
        """
        Проверяет, что указанный путь существует и является директорией

        Иначе ошибка
        :raise BashNoSuchFileOrDirectoryError, BashNotADirectoryError:
        """


        if not self._params:
            return []

        # We know: there is only one parameter
        path = self._params[0]
        command_name = self.name()

        # Здесь все ошибки являются критическими, поэтому raise
        if not fs.properties.existing_path(path):
            raise BashNoSuchFileOrDirectoryError(name=command_name, filename=path)
        elif not fs.properties.is_dir(path):
            raise BashNotADirectoryError(name=command_name, filename=path)

        return []
