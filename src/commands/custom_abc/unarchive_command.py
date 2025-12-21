from abc import ABC, abstractmethod
from pathlib import Path

from src.core.errors import BashError, BashNoSuchFileOrDirectoryError, BashCommandError
from src.terminal.command import BashCommand
from src.terminal.file_system.fs import fs
from src.terminal.file_system.resolve_path import resolve_path


class UnarchiveBashCommand(BashCommand, ABC):
    """Родительский класс для команд распаковки архивов"""

    @abstractmethod
    def is_supported_file(self, file: Path) -> bool:
        """Проверяет, поддерживается ли формат архива."""
        pass

    @abstractmethod
    def unarchive(self, archive: Path, extract_dir: Path) -> None:
        """Распакоууука"""
        pass

    def _get_extract_dir(self):
        """Генерирует уникальное имя директории для распаковки (с учётом существующих)"""
        tries = 0
        while True:
            maybe_name = ".".join(self._params[0].removesuffix(".gz").split(".")[:-1]) + (
                str(tries) if tries > 0 else "")
            if fs.properties.existing_path(maybe_name):
                tries += 1
            else:
                return maybe_name

    def _exec(self) -> tuple[list[BashError], str | None] | None:
        """Выполняет распаковку архива в новую директорию"""
        archive = resolve_path(self._params[0])
        extract_dir = resolve_path(self._get_extract_dir())
        self.unarchive(archive, extract_dir)
        return [], f"{self.name()}: {archive.name} -> {extract_dir.name}"

    @property
    def _max_params_count(self) -> int | None:
        return 1

    def _validate_params(self) -> list[BashError]:
        """Проверяет существование архива и поддержку его формата"""
        if not fs.properties.existing_path(self._params[0]):
            raise BashNoSuchFileOrDirectoryError(name=self.name(), filename=self._params[0])

        elif not self.is_supported_file(resolve_path(self._params[0])):
            raise BashCommandError(name=self.name(), msg="it's not a supported file")
        return []
