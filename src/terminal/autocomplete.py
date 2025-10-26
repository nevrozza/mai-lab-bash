import readline

from src.terminal.command import BashCommand


class Autocomplete:
    @classmethod
    def enable(cls):
        # Регистрация `Tab` для автокомплита
        readline.parse_and_bind('tab: complete')
        readline.parse_and_bind('bind ^I rl_complete')  # MacOS...
        readline.set_completer(cls._autocompleter)
        readline.set_completer_delims(' ')  # По умолчанию там есть другие знаки (!~*...) из-за чего хрень выходит

        # В Ubuntu (или в терминале MacOS) в ситуации где у нас есть 2 файла в директории [p1, p2],
        # и мы вводим команду (например catman), но с автокомплитом:
        # 'catma' -> 'catman ' -> 'catman p' -> 'catman p'+подсказки
        # Т.е. Подсказки выводятся после второго таба,
        # но что важно: отсчёт табов начинается после `развилки`
        #
        # В текущей реализации программы это не так, а вот так:
        # 'catma' -> 'catman ' -> 'catman p'+подсказки
        # Причём: 'catman ' -> 'catman p' -> 'catman p'+подсказки (нет единообразия((
        # Т.е. отсчёт табов введёт себя по-другому(
        #
        # Можно было бы написать свою реализацию вывода подсказок, но, к сожалению,
        # Из-за особенностей MacOS функция, которая позволяет это сделать, игнорится =)))
        # https://github.com/oils-for-unix/oils/pull/235
        # readline.set_completion_display_matches_hook()
        #
        # Double `Tab` workaround
        # readline.get_completion_type() -> 63 # ord("?") if doubleTab
        # readline.get_completion_type() -> 9 # ord("\t") if singleTab
        # print(readline.get_completion_type())

        cls._current_suggestions = []

    @classmethod
    def _autocompleter(cls, _: str, state: int) -> str | None:
        """
        !!! Используется для `readline.set_completer` !!!

        :param _: Был text, но безопаснее использовать `readline.get_line_buffer()`
        :param state: Итерация прохода по suggestions
        :return: Одно из предложений или None
        """

        # Эта функция вызывается после нажатия `Tab` до тех пор, пока не получит None
        # Иначе происходит инкремент state
        # Поэтому делаем проверку state == 0
        if not state:
            input_line = readline.get_line_buffer()

            # В bash ведущие пробелы не роляют
            leading_spaces = len(input_line) - len(input_line.lstrip())
            input_line = input_line.lstrip()

            begin = readline.get_begidx() - leading_spaces
            end = readline.get_endidx() - leading_spaces

            # Текст, который мы сейчас дополняем
            being_completed = input_line[begin:end]

            if not input_line:
                # Пустая строка -> показываем все команды
                cls._current_suggestions = list(BashCommand.get_all_commands().keys())
            elif begin == 0:
                # Первое слово -> дополняем команды
                suggestions = [cmd for cmd in BashCommand.get_all_commands()
                               if cmd.startswith(being_completed)]
                if len(suggestions) == 1:
                    # Разветвление необходимо, чтобы добавить пробел к полностью введённому слову
                    cls._current_suggestions = [suggestions[0] + " "]
                else:
                    cls._current_suggestions = suggestions

            else:
                # Обработка остальных параметров (следующие слова после первого!)
                dir_content = ["p1 ", "p2 "]  # , "xx "
                if being_completed:  # Если мы начали писать имя файла/директории
                    cls._current_suggestions = [d for d in dir_content if d.startswith(being_completed)]
                else:
                    cls._current_suggestions = dir_content

        if state < len(cls._current_suggestions):
            return cls._current_suggestions[state]
        else:
            return None
