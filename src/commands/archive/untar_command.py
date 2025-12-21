import tarfile
from pathlib import Path

from src.commands.custom_abc.unarchive_command import UnarchiveBashCommand


class UntarBashCommand(UnarchiveBashCommand):

    def is_supported_file(self, file: Path) -> bool:

        try:
            return tarfile.is_tarfile(file)
        except tarfile.TarError:
            return False

    def unarchive(self, archive: Path, extract_dir: Path) -> None:
        with tarfile.open(archive, "r:gz") as tar:
            tar.extractall(extract_dir)

    @classmethod
    def name(cls) -> str:
        return "untar"
