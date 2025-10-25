from abc import ABC


class Command(ABC):
    pass


class LsCommand(Command):
    pass


class CopyCommand(Command):
    pass


class MeowCommand(Command):
    pass


for i in Command.__subclasses__():
    print(i.__name__.removesuffix("Command").lower(), end=" ")

quit(0)
