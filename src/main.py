from src.terminal.command import BashCommand
from src.terminal.terminal import Terminal


def main() -> None:
    """
    Обязательнная составляющая программ, которые сдаются. Является точкой входа в приложение
    :return: Данная функция ничего не возвращает
    """
    terminal = Terminal()
    print("Double `Tab` for show all commands")
    while True:
        input(">")


if __name__ == "__main__":
    main()
