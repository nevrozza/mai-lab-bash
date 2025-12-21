import tarfile
from pathlib import Path

from src.commands.custom_abc.archive_command import ArchiveBashCommand


class TarBashCommand(ArchiveBashCommand):
    @property
    def file_extension(self) -> str:
        return "tar.gz"

    def archive(self, folder: Path, zip_name: str) -> None:
        with tarfile.open(zip_name, "w:gz") as tar:
            for f in folder.iterdir():
                tar.add(f, arcname=f.name)

    @classmethod
    def name(cls) -> str:
        return "tar"
