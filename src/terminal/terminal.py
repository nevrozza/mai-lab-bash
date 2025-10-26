import readline

from src.terminal.command import BashCommand


# https://docs-python.ru/standart-library/modul-readline-python/
class Terminal:
    def __init__(self):
        # Импоритруем команды
        BashCommand.import_all_commands()

        # Регистрация `Tab` для автокомплита
        readline.parse_and_bind('tab: complete')
        readline.parse_and_bind('bind ^I rl_complete')  # MacOS...
        readline.set_completer(self._autocompleter)
        readline.set_completer_delims(' ')  # По умолчанию там есть другие знаки (!~*...) из-за чего

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

        self._current_suggestions = []

    def _autocompleter(self, _: str, state: int) -> str | None:
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
                self._current_suggestions = list(BashCommand.get_all_commands().keys())
            elif begin == 0:
                # Первое слово -> дополняем команды
                suggestions = [cmd for cmd in BashCommand.get_all_commands()
                               if cmd.startswith(being_completed)]
                if len(suggestions) == 1:
                    # Разветвление необходимо, чтобы добавить пробел к полностью введённому слову
                    self._current_suggestions = [suggestions[0] + " "]
                else:
                    self._current_suggestions = suggestions

            else:
                # Обработка остальных параметров (следующие слова после первого!)
                dir_content = ["p1 ", "p2 ", "xx "]
                if being_completed:  # Если мы начали писать имя файла/директории
                    self._current_suggestions = [d for d in dir_content if d.startswith(being_completed)]
                else:
                    self._current_suggestions = dir_content

        if state < len(self._current_suggestions):
            return self._current_suggestions[state]
        else:
            return None
