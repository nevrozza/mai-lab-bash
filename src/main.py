from src.core.logging import Logger
from src.terminal.terminal import Terminal


def main() -> None:
    """
    Обязательнная составляющая программ, которые сдаются. Является точкой входа в приложение
    :return: Данная функция ничего не возвращает
    """
    Logger.setup_shell_logger()
    terminal = Terminal()
    terminal.cycle_input()


if __name__ == "__main__":
    main()
