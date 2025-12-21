from src.commands.custom_abc.undoable_command import UndoableBashCommand
from src.core.errors import BashError, BashCommandError
from src.terminal.command import BashCommand
from src.terminal.history import HistoryManager, HistoryLine
from src.utils.could_be_undo import could_be_undo


class UndoBashCommand(BashCommand):
    @property
    def _max_params_count(self) -> int | None:
        return 1

    def _exec(self) -> tuple[list[BashError], str | None] | None:
        if self._params:
            num = int(self._params[0])
            history_line = HistoryManager.get_line_by_num(num)
        else:
            history_line = next((line for line in reversed(HistoryManager.history) if could_be_undo(line)), None)

        return self.__run_undo(history_line), None

    def __run_undo(self, history_line: HistoryLine) -> list[BashError]:
        # noinspection PyTypeChecker
        command: UndoableBashCommand = BashCommand.get_all_commands()[history_line.command_name]
        if command and could_be_undo(history_line):
            errors = command.undo(history_line)
        else:
            raise BashCommandError(name=self.name(), msg="can't undo")
        HistoryManager.mark_undo(history_line)
        return errors

    def _validate_params(self) -> list[BashError]:
        if not ((not self._params) or (len(self._params) == 1 and self._params[0].isdigit())):
            raise BashCommandError(name=self.name(), msg="you have to use number for undo")
        return []
