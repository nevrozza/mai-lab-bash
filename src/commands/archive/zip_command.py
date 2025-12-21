from pathlib import Path
from zipfile import ZipFile

from src.commands.custom_abc.archive_command import ArchiveBashCommand


class ZipBashCommand(ArchiveBashCommand):
    @property
    def file_extension(self) -> str:
        return "zip"

    def archive(self, folder: Path, zip_name: str) -> None:
        with ZipFile(zip_name, "w") as zf:
            for file in folder.iterdir():
                zf.write(file, arcname=file.name)

    @classmethod
    def name(cls) -> str:
        return "zip"
