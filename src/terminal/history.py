import json
from dataclasses import dataclass, replace
from enum import Enum
from pathlib import Path

from src.core.config import BashConfig
from src.core.errors import BashError
from src.core.logging import log
from src.terminal.file_system.fs import fs


class HistoryLineStatus(Enum):
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"
    UNDO = "UNDO"


@dataclass(frozen=True)
class HistoryLine:
    num: int
    command_name: str
    command_line: str
    status: HistoryLineStatus
    wd: str


class HistoryManager:
    @classmethod
    def initialize(cls):
        cls.history: list[HistoryLine] = []
        cls._history_path = Path(
            BashConfig.HISTORY_FILE_NAME
        ).resolve()  # resolve -> не зависим от cwd, т.к. absolute path

        if not fs.properties.existing_path(cls._history_path):
            cls._create_history_file()

        cls._next_num = 1
        cls._load()

    @classmethod
    def _create_history_file(cls):
        cls._history_path.touch()
        cls._history_path.write_text("[]")  # Empty json array

    @classmethod
    def _load(cls):
        try:
            with open(cls._history_path, encoding='utf-8') as f:
                data = json.load(f)
                cls.history = [
                    HistoryLine(
                        num=item['num'],
                        command_name=item["name"],
                        command_line=item['command'],
                        status=HistoryLineStatus(item['status']),
                        wd=item['wd']
                    )
                    for item in data
                ]
        except Exception as e:
            log(BashError(f"failed to load history from {cls._history_path}: {e}"))
            cls._create_history_file()
            cls.history = []
        finally:
            cls._next_num = (cls.history[-1].num + 1) if cls.history else 1

    @classmethod
    def _save(cls):
        try:
            data = [
                {
                    'num': line.num,
                    'name': line.command_name,
                    'command': line.command_line,
                    'status': line.status.value,
                    'wd': line.wd
                }
                for line in cls.history
            ]
            with open(cls._history_path, 'r+', encoding='utf-8') as f:
                # https://stackoverflow.com/questions/12309269/how-do-i-write-json-data-to-a-file
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            log(BashError(f"failed to save history to {cls._history_path}: {e}"))

    @classmethod
    def add_command(cls, command_name: str, command_line: str, is_error: bool, wd: str):
        new_line = HistoryLine(
            num=cls._next_num,
            command_line=command_line,
            status=HistoryLineStatus.ERROR if is_error else HistoryLineStatus.SUCCESS,
            wd=wd,
            command_name=command_name
        )
        cls.history.append(new_line)
        cls._next_num += 1
        cls._save()

    @classmethod
    def get_line_by_num(cls, num: int) -> HistoryLine | None:
        return next((line for line in reversed(cls.history) if line.num == num), None)

    @classmethod
    def mark_undo(cls, history_line):
        for i in range(len(cls.history) - 1, -1, -1):
            if cls.history[i] == history_line:
                cls.history[i] = replace(history_line, status=HistoryLineStatus.UNDO)
                cls._save()
                break
