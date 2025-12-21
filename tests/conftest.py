# https://docs.pytest.org/en/stable/how-to/tmp_path.html
import os

import pytest

from src.commands.import_default_commands import import_default_commands
from src.core.logging import Logger
from src.terminal.file_system.fs import fs
from src.terminal.file_system.resolve_path import resolve_path
from src.terminal.history import HistoryManager


@pytest.fixture
def temp_dir(tmp_path):
    import_default_commands()
    cwd = resolve_path(fs.cwd_str())
    os.chdir(tmp_path)
    Logger.setup_shell_logger()
    HistoryManager.initialize()
    yield tmp_path
    os.chdir(cwd)
