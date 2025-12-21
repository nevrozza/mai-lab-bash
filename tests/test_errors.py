import pytest

from src.commands.files_content.cat_command import CatBashCommand
from src.commands.navigation.cd_command import CDBashCommand
from src.commands.undoables.cp_command import CPBashCommand
from src.commands.undoables.mv_command import MVBashCommand
from src.commands.undoables.rm_command import RMBashCommand
from src.core.errors import BashNoSuchFileOrDirectoryError, BashNotADirectoryError, BashCommandError


def test_cd_no_such_file(temp_dir):
    with pytest.raises(BashNoSuchFileOrDirectoryError):
        cmd = CDBashCommand(["no_such_file"], "")
        cmd.execute()


def test_cd_not_a_dir(temp_dir):
    filename = "file.txt"
    (temp_dir / filename).write_text("hello")
    with pytest.raises(BashNotADirectoryError):
        cmd = CDBashCommand([filename], "")
        cmd.execute()


def test_cat_directory(temp_dir):
    dir_name = "dir"
    (temp_dir / dir_name).mkdir()
    cmd = CatBashCommand([dir_name], "")
    errors, _ = cmd.execute()
    assert any("Is a directory" in str(e) for e in errors)


def test_cp_dir_without_r(temp_dir):
    src = temp_dir / "src"
    src.mkdir()
    (src / "f.txt").write_text("x")
    dist = temp_dir / "dist"
    dist.mkdir()
    with pytest.raises(BashCommandError, match="-r not specified"):
        CPBashCommand([src.name, dist.name], "").execute()


def test_rm_dir_without_r(temp_dir):
    d = temp_dir / "to_delete"
    d.mkdir()
    with pytest.raises(BashCommandError, match=r"'-r' not specified"):
        RMBashCommand([d.name], "").execute()


def test_rm_no_such_file(temp_dir):
    cmd = RMBashCommand(["no_such_file"], "")
    errors, _ = cmd.execute()
    assert any("No such file or directory" in str(e) for e in errors)


def test_cp_no_args(temp_dir):
    with pytest.raises(BashCommandError, match="missing file operand"):
        CPBashCommand([], "").execute()


def test_mv_one_arg(temp_dir):
    with pytest.raises(BashCommandError, match="missing destination"):
        MVBashCommand(["only_one"], "").execute()


def test_rm_protection(temp_dir):
    with pytest.raises(BashCommandError, match="current or parent directory"):
        RMBashCommand([".", "-r"], "").execute()
