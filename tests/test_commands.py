import pathlib
import shutil

from src.commands.archive.tar_command import TarBashCommand
from src.commands.archive.untar_command import UntarBashCommand
from src.commands.archive.unzip_command import UnzipBashCommand
from src.commands.archive.zip_command import ZipBashCommand
from src.commands.files_content.cat_command import CatBashCommand
from src.commands.files_content.grep_command import GrepBashCommand
from src.commands.history.history_command import HistoryBashCommand
from src.commands.history.undo_command import UndoBashCommand
from src.commands.navigation.cd_command import CDBashCommand
from src.commands.navigation.ls_command import LSBashCommand
from src.commands.undoables.cp_command import CPBashCommand
from src.commands.undoables.mv_command import MVBashCommand
from src.commands.undoables.rm_command import RMBashCommand
from src.terminal.history import HistoryManager
from src.terminal.terminal import Terminal


def test_cd_command(temp_dir):
    t_dir = temp_dir / "test_dir"
    t_dir.mkdir()
    CDBashCommand(["test_dir"], "").execute()
    assert pathlib.Path.cwd() == t_dir


def ls_command_test(temp_dir, params):
    (temp_dir / "file1").touch()
    (temp_dir / "file2").touch()
    (temp_dir / ".hidden").touch()
    (temp_dir / "visible").touch()
    _, (_, output) = LSBashCommand(params, "").execute()
    return output


def test_ls_command(temp_dir):
    output = ls_command_test(temp_dir, [])
    assert ".hidden" not in output
    assert "visible" in output
    assert "file1" in output
    assert "file2" in output


def test_ls_a(temp_dir):
    output = ls_command_test(temp_dir, ["-a"])
    assert ".hidden" in output
    assert "visible" in output
    assert "file1" in output
    assert "file2" in output


def test_ls_l(temp_dir):
    output = ls_command_test(temp_dir, ["-l"])
    lines = output.strip().split("\n")
    assert len(lines) >= 2  # total + entry
    assert "visible" in lines[-1]


def test_cat_command(temp_dir):
    file = temp_dir / "test.txt"
    text = "\n".join(f"line{i}" for i in range(100))
    file.write_text(text)
    _, (_, output) = CatBashCommand(["test.txt"], "").execute()
    assert output == text


def test_cp_command(temp_dir):
    src = temp_dir / "src.txt"
    dst = temp_dir / "dst.txt"
    text = "hello"
    src.write_text(text)
    CPBashCommand([src.name, dst.name], "").execute()
    assert dst.read_text() == text


def test_cp_into_dir(temp_dir):
    src = temp_dir / "src.txt"
    dist = temp_dir / "dist"
    dist.mkdir()
    text = "copyme"
    src.write_text(text)
    CPBashCommand([src.name, dist.name], "").execute()
    assert (dist / src.name).read_text() == text


def test_cp_dir_with_r(temp_dir):
    src = temp_dir / "src"
    src.mkdir()
    filename, text = "f.txt", "x"
    (src / filename).write_text(text)
    dist = temp_dir / "dist"
    dist.mkdir()
    CPBashCommand(["-r", src.name, dist.name], "").execute()
    assert (dist / src.name / filename).read_text() == text


def test_mv_command(temp_dir):
    src = temp_dir / "old.txt"
    dist = temp_dir / "new.txt"
    text = "moved"
    src.write_text(text)
    MVBashCommand([src.name, dist.name], "").execute()
    assert not src.exists()
    assert dist.read_text() == text


def test_mv_into_dir(temp_dir):
    src = temp_dir / "file.txt"
    text = "move into dir"
    src.write_text(text)
    dist = temp_dir / "target"
    dist.mkdir()
    MVBashCommand([src.name, dist.name], "").execute()
    assert not src.exists()
    assert (dist / src.name).read_text() == text


def test_mv_multiple_files(temp_dir):
    (temp_dir / "a").touch()
    (temp_dir / "b").touch()
    dist = temp_dir / "dist"
    dist.mkdir()
    MVBashCommand(["a", "b", "dist"], "").execute()
    assert not (temp_dir / "a").exists()
    assert not (temp_dir / "b").exists()
    assert (dist / "a").exists()
    assert (dist / "b").exists()


def test_rm_command(temp_dir):
    f = temp_dir / "to_delete.txt"
    f.write_text("delete me")
    RMBashCommand([f.name], "").execute()
    assert not f.exists()
    assert (temp_dir / ".trash" / f.name).exists()


def test_rm_dir_with_r_flag(temp_dir, monkeypatch):
    d = temp_dir / "to_del"
    d.mkdir()
    (d / "inner").write_text("x")
    # https://stackoverflow.com/questions/35851323/how-to-test-a-function-with-input-call
    monkeypatch.setattr("builtins.input", lambda _: "y")
    RMBashCommand(["-r", d.name], "").execute()
    assert not d.exists()
    assert (temp_dir / ".trash" / d.name).exists()


def test_grep_command(temp_dir):
    file = temp_dir / "test.txt"
    file.write_text("Apple\nbanana")
    _, (_, output) = GrepBashCommand(["Apple", "test.txt"], "").execute()
    assert output is not None
    assert "test.txt:1 Apple" in output


def test_grep_ignore_case(temp_dir):
    file = temp_dir / "test.txt"
    file.write_text("Apple\nbanana")
    _, (_, output) = GrepBashCommand(["apple", "-i", "test.txt"], "").execute()
    assert output is not None
    assert "test.txt:1 Apple" in output


def test_zip_commands(temp_dir):
    folder = temp_dir / "archive_test"
    folder.mkdir()
    (folder / "file1.txt").write_text("content1")
    (folder / "file2.txt").write_text("content2")

    # zip
    _, (_, out) = ZipBashCommand(["archive_test"], "").execute()
    assert out is not None
    assert "zip created" in out
    assert (temp_dir / "archive_test.zip").exists()

    # unzip
    shutil.rmtree(folder)
    _, (_, out) = UnzipBashCommand(["archive_test.zip"], "").execute()
    assert out is not None
    assert "unzip" in out
    assert (temp_dir / "archive_test" / "file1.txt").read_text() == "content1"
    assert (temp_dir / "archive_test" / "file2.txt").read_text() == "content2"


def test_tar_commands(temp_dir):
    folder = temp_dir / "tar_test"
    folder.mkdir()
    text = "text"
    (folder / "doc.txt").write_text(text)

    # tar
    tar_cmd = TarBashCommand(["tar_test"], "")
    _, (_, out) = tar_cmd.execute()
    assert out is not None
    assert "tar created" in out
    assert (temp_dir / "tar_test.tar.gz").exists()

    # untar
    shutil.rmtree(folder)
    untar_cmd = UntarBashCommand(["tar_test.tar.gz"], "")
    _, (_, out) = untar_cmd.execute()
    assert out is not None
    assert "untar" in out
    assert (temp_dir / "tar_test" / "doc.txt").read_text() == text


def test_history_command(temp_dir):
    HistoryManager.add_command("элэс", "элэс", is_error=True, wd=str(temp_dir))
    HistoryManager.add_command("cd", "cd ..", is_error=False, wd=str(temp_dir))

    _, (_, output) = HistoryBashCommand([], "history").execute()
    assert output is not None
    lines = output.split("\n")
    assert len(lines) == 2
    assert "элэс" in lines[0]
    assert "cd .." in lines[1]


def test_undo_command(temp_dir):
    rm = temp_dir / "rm"
    cp = temp_dir / "cp"
    mv = temp_dir / "mv"
    other = temp_dir / "other"
    [d.mkdir() for d in (rm, cp, other, mv)]

    Terminal._execute_commands(
        [
            RMBashCommand(["-rf", rm.name], f"rm -rf {rm.name}"),
            CPBashCommand(["-r", cp.name, other.name], f"cp -r {cp.name} {other.name}"),
            MVBashCommand([mv.name, other.name], f"mv {mv.name} {other.name}"),
        ]
    )

    assert not rm.exists()
    assert (temp_dir / ".trash" / rm.name).exists()
    assert not mv.exists()
    assert (other / mv.name).exists()
    assert cp.exists()
    assert (other / cp.name).exists()

    UndoBashCommand([], "").execute()
    UndoBashCommand([], "").execute()
    UndoBashCommand([], "").execute()

    assert rm.exists()
    assert not (temp_dir / ".trash" / rm.name).exists()
    assert mv.exists()
    assert not (other / mv.name).exists()
    assert cp.exists()
    assert not (other / cp.name).exists()
