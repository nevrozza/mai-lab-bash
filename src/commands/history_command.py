from src.core.errors import BashError, BashCommandError
from src.terminal.command import BashCommand
from src.terminal.history import HistoryManager, HistoryLineStatus
from src.utils.print_builder import PrintBuilder


class HistoryBashCommand(BashCommand):
    @property
    def _max_params_count(self) -> int | None:
        return 1

    def _exec(self) -> str:
        print_builder = PrintBuilder()
        start = -int(self._params[0]) if self._params else 0
        history = HistoryManager.history[start:]
        for line in history:
            if line.status != HistoryLineStatus.UNDO:
                print_builder.append(f"{line.num:^5} {line.command_line}")
        return print_builder.get()

    def _validate_params(self) -> list[BashError]:
        if not ((not self._params) or (len(self._params) == 1 and self._params[0].isdigit())):
            raise BashCommandError(name=self._name(), msg="you have to use number for history")
        return []
