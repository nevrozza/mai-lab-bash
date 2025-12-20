from src.core.errors import BashError
from src.terminal.command import BashCommand
from src.utils.validate_params import cp_mv_validate_params


class CPBashCommand(BashCommand):
    def _exec(self) -> str:
        pass

    def _validate_params(self) -> list[BashError]:
        return cp_mv_validate_params(params=self._params, command_name=self._name())
