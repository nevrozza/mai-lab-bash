class BashError(Exception):
    """Класс кастомных ошибок CLI"""
    pass


class BashSyntaxError(BashError):
    def __init__(self):
        super().__init__("syntax error!")


class BashNoSupportForLongFlagsError(BashError):
    def __init__(self):
        super().__init__("there is no support for long flags yet.")


class BashCommandError(BashError):
    """
    Дефолтная ошибка для команд

    **Пример:** `cd: too many arguments`
    """
    def __init__(self, name: str, msg: str):
        super().__init__(f"{name}: {msg}")


class BashInvalidFlagError(BashCommandError):  # Invalid option
    def __init__(self, name: str, flag: str, supported: str):
        super().__init__(name=name,
                         msg=f"-{flag}: invalid option" + (f" (supported: -{" -".join(supported)})" if supported else ""))


class BashMissingDestinationFileOperandError(BashCommandError):
    def __init__(self, name: str, prev_path: str):
        super().__init__(name=name, msg=f"missing destination file operand after '{prev_path}'")


class BashMissingFileOperandError(BashCommandError):
    def __init__(self, name: str):
        super().__init__(name=name, msg="missing file operand")


class BashMoreParamsThenExpectedError(BashCommandError):
    def __init__(self, name: str):
        super().__init__(name=name, msg="too many arguments")


class BashNoSuchFileOrDirectoryError(BashCommandError):
    def __init__(self, name: str, filename: str):
        super().__init__(name=name, msg=f"cannot access '{filename}': No such file or directory")


class BashNotADirectoryError(BashCommandError):
    def __init__(self, name: str, filename: str):
        super().__init__(name=name, msg=f"{filename}: Not a directory")
