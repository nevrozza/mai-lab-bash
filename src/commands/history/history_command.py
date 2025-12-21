from src.core.errors import BashError, BashCommandError
from src.terminal.command import BashCommand
from src.terminal.history import HistoryManager, HistoryLineStatus
from src.utils.could_be_undo import could_be_undo
from src.utils.print_builder import PrintBuilder


class HistoryBashCommand(BashCommand):
    """Выводит историю выполненных команд (можно передать N)"""

    @property
    def _max_params_count(self) -> int | None:
        return 1

    def _exec(self) -> tuple[list[BashError], str | None] | None:
        """Формирует вывод истории: номер, метка того, что отменяется (*) и сама команда"""
        print_builder = PrintBuilder()
        start = -int(self._params[0]) if self._params else 0
        history = HistoryManager.history[start:]
        for line in history:
            if line.status != HistoryLineStatus.UNDO:
                print_builder.append(
                    f"{line.num:^5} {"*" if (could_be_undo(line)) else " "} {line.command_line}")
        return [], print_builder.get()

    def _validate_params(self) -> list[BashError]:
        """Проверяет, что параметр (если есть) – это число"""
        if not ((not self._params) or (len(self._params) == 1 and self._params[0].isdigit())):
            raise BashCommandError(name=self.name(), msg="you have to use number for history")
        return []
