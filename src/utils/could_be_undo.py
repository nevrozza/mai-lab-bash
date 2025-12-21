from src.commands.custom_abc.undoable_command import UndoableBashCommand
from src.terminal.history import HistoryLine, HistoryLineStatus


def could_be_undo(line: HistoryLine):
    return line.command_name in UndoableBashCommand.undoable_commands and line.status == HistoryLineStatus.SUCCESS
