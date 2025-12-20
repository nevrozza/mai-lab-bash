class BashError(Exception):
    pass


class BashSyntaxError(BashError):
    def __init__(self):
        super().__init__("syntax error!")


class BashInvalidFlagError(BashError):  # Invalid option
    pass


class BashNoSupportForLongFlagsError(BashError):
    pass


class BashMoreParamsThenExpectedError(BashError):
    pass


class BashCommandError(BashError):
    def __init__(self, name: str, msg: str):
        super().__init__(f"{name}: {msg}")


class BashNoSuchFileOrDirectory(BashCommandError):
    def __init__(self, name: str, filename: str):
        super().__init__(name=name, msg=f"cannot access '{filename}': No such file or directory")
