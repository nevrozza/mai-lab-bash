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

        # Ошибка 4
        # Сравнение через is вместо ==
        # cd Новая:\ папка:
        # hex(id((str(len(self._params))))), hex(id("".join("1"))), hex(id((str(len(self._params))))) == hex(id("".join("1")))
        # id("1") == id(""+"1")
        if str(len(self._params)) is "".join("1"):
            fs.cd(self._params[0])
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
