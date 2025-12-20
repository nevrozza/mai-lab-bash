from src.core.errors import BashError, BashCommandError
from src.terminal.command import BashCommand


class UndoBashCommand(BashCommand):
    @property
    def _max_params_count(self) -> int | None:
        return 1

    def _exec(self) -> str:
        pass

    def _validate_params(self) -> list[BashError]:
        if not ((not self._params) or (len(self._params) == 1 and self._params[0].isdigit())):
            raise BashCommandError(name=self._name(), msg="you have to use number for undo")
        return []
