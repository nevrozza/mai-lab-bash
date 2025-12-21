from abc import ABC, abstractmethod
from pathlib import Path

from src.core.errors import BashError, BashCommandError, BashNoSuchFileOrDirectoryError, BashNotADirectoryError
from src.terminal.command import BashCommand
from src.terminal.file_system.fs import fs
from src.terminal.file_system.resolve_path import resolve_path


class ArchiveBashCommand(BashCommand, ABC):

    @property
    @abstractmethod
    def file_extension(self) -> str:
        pass

    @abstractmethod
    def archive(self, folder: Path, zip_name: str) -> None:
        pass

    def _exec(self) -> tuple[list[BashError], str | None] | None:
        folder = resolve_path(self._params[0])
        zip_name = self._params[1] if len(self._params) > 1 else f"{folder.name}.{self.file_extension}"
        self.archive(folder, zip_name)
        return [], f"{self.name()} created: {zip_name}"

    @property
    def _max_params_count(self) -> int | None:
        return 2

    def _validate_params(self) -> list[BashError]:
        if not fs.properties.existing_path(self._params[0]):
            raise BashNoSuchFileOrDirectoryError(name=self.name(), filename=self._params[0])
        elif not fs.properties.is_dir(self._params[0]):
            raise BashNotADirectoryError(name=self.name(), filename=self._params[0])
        return []
