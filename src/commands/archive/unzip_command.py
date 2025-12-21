import zipfile
from pathlib import Path
from zipfile import ZipFile

from src.commands.custom_abc.unarchive_command import UnarchiveBashCommand


class UnzipBashCommand(UnarchiveBashCommand):

    def is_supported_file(self, file: Path) -> bool:
        return zipfile.is_zipfile(file)

    def unarchive(self, archive: Path, extract_dir: Path) -> None:
        with ZipFile(archive) as zf:
            zf.extractall(extract_dir)

    @classmethod
    def name(cls) -> str:
        return "unzip"
