from abc import ABC, abstractmethod
from pathlib import Path

from src.core.errors import BashError, BashNoSuchFileOrDirectoryError, BashNotADirectoryError
from src.terminal.command import BashCommand
from src.terminal.file_system.fs import fs
from src.terminal.file_system.resolve_path import resolve_path


class ArchiveBashCommand(BashCommand, ABC):
    """Родительский класс для команд архивации директорий"""

    @property
    @abstractmethod
    def file_extension(self) -> str:
        """Расширение создаваемого архива (``zip`` или ``tar.gz``)"""
        pass

    @abstractmethod
    def archive(self, folder: Path, zip_name: str) -> None:
        """Создаёт архив из указанной директории"""
        pass

    def _get_zip_name(self, folder: Path) -> str:
        """Генерирует уникальное имя архива, избегая конфликтов с существующими файлами"""
        tries = 0
        while True:
            maybe_name = (self._params[1] if len(self._params) > 1 else (f"{folder.name}"
                                                                         + (str(tries) if tries > 0 else "")
                                                                         + f".{self.file_extension}"))
            if fs.properties.existing_path(maybe_name):
                tries += 1
            else:
                return maybe_name

    def _exec(self) -> tuple[list[BashError], str | None] | None:
        """Выполняет архивацию указанной директории"""
        folder = resolve_path(self._params[0])
        zip_name = self._get_zip_name(folder)
        self.archive(folder, zip_name)
        return [], f"{self.name()} created: {zip_name}"

    @property
    def _max_params_count(self) -> int | None:
        return 2

    def _validate_params(self) -> list[BashError]:
        """Проверяет, что первый аргумент – существующая директория"""
        if not fs.properties.existing_path(self._params[0]):
            raise BashNoSuchFileOrDirectoryError(name=self.name(), filename=self._params[0])
        elif not fs.properties.is_dir(self._params[0]):
            raise BashNotADirectoryError(name=self.name(), filename=self._params[0])
        return []
