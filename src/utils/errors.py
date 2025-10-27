class BashError(Exception):
    pass


class BashSyntaxError(Exception):
    pass


class BashInvalidFlagError(Exception):  # Invalid option
    pass


class BashNoSupportForLongFlagsError(Exception):
    pass


class BashMoreParamsThenExpectedError(Exception):
    pass


class BashCommandError(Exception):
    def __init__(self, name: str, msg: str):
        self.name = name
        self.msg = msg
