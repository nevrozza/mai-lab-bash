import readline

from src.terminal.command import BashCommand
from src.terminal.fs import FS
from src.utils.quoting_type import QuotingType


class Autocomplete:
    # I f****d this API

    @classmethod
    def enable(cls):
        # Регистрация `Tab` для автокомплита
        readline.parse_and_bind('tab: complete')
        readline.parse_and_bind('bind ^I rl_complete')  # MacOS...
        readline.set_completer(cls._autocompleter)
        readline.set_completer_delims(' ;')  # По умолчанию там есть другие знаки (!~*...) из-за чего хрень выходит

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

    @staticmethod
    def _get_completion_word(line: str) -> tuple[bool, str]:
        line = line.lstrip()

        # parenthesis_stack: list[str] = [] not yet implemented =/

        opened_double_quote = None
        opened_single_quote = None
        space = 0

        is_command = True
        is_command_entered = False

        words: list[str] = []

        # TODO: refactor
        for index, char in enumerate(line):
            if char != ' ':
                is_command_entered = True

            if char == "'":
                if opened_single_quote:
                    words.append(line[opened_single_quote:index])
                    opened_single_quote = None
                else:
                    opened_single_quote = index
            elif char == '"':
                if opened_double_quote:
                    words.append(line[opened_double_quote:index])
                    opened_double_quote = None
                else:
                    opened_double_quote = index
            elif char == '\\' and not opened_double_quote and not opened_single_quote:
                if (index + 1 < len(line)) and line[index + 1] == ' ':
                    opened_single_quote = space
            elif char == ' ':
                if is_command_entered:
                    is_command = False

                if space == 0:
                    words.append(line[space:index])
                    space = index
                elif not opened_double_quote and not opened_single_quote:
                    words.append(line[space:index])
                    space = index
            elif char == ';' and not opened_single_quote and not opened_double_quote:
                is_command = True
                is_command_entered = False
                words = []
                space = index + 1
        end_el = line[space:].lstrip()
        if end_el == ";":
            end_el = ""
        words.append(end_el)
        return is_command, words[-1]

    @classmethod
    def _autocompleter(cls, completion_scope: str, state: int) -> str | None:
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

            # Текст, который мы сейчас дополняем
            line = readline.get_line_buffer()[:readline.get_endidx()]
            is_command, being_completed = cls._get_completion_word(line)

            if being_completed and being_completed[0] in ('"', "'"):
                quoting_type = QuotingType(being_completed[0])
            elif '\\' in being_completed:
                quoting_type = QuotingType.ESCAPING_TYPE
            else:
                quoting_type = QuotingType.SINGLE_QUOTE

            if is_command:
                # Предлагаем команды
                suggestions = [cmd for cmd in BashCommand.get_all_commands()
                               if cmd.startswith(being_completed)]
                cls._current_suggestions = suggestions
            else:
                # Предлагаем содержимое pwd
                cls._current_suggestions = cls._get_relevant_dir_content(being_completed=being_completed,
                                                                         completion_scope=completion_scope,
                                                                         quoting_type=quoting_type)

        if state < len(cls._current_suggestions):
            if len(cls._current_suggestions) == 1:
                return cls._current_suggestions[0] + " "  # Добавляем пробел после ставки

            return cls._current_suggestions[state]
        else:
            return None

    @classmethod
    def _get_relevant_dir_content(cls, being_completed: str, completion_scope: str, quoting_type: QuotingType):
        dir_content = [FS.normalize_name(p.name, quoting_type=quoting_type) for p in
                       FS.ls("") if not FS.is_hidden(p)]

        if being_completed:
            return [
                cls._cut_normalized_name_for_complete(name=p, being_completed=being_completed,
                                                      completion_scope=completion_scope)
                for p in dir_content if p.startswith(being_completed) or (p.startswith("'" + being_completed))]
        else:
            return dir_content

    @classmethod
    def _cut_normalized_name_for_complete(cls, name: str, being_completed: str, completion_scope: str):
        length = len(being_completed)
        is_on_gap = len(name) >= length and name[length + 1] == ' '
        is_without_quote_but_should = being_completed[0] != "'" and name[0] == "'"

        if is_without_quote_but_should:  # if there is no quote before word with quotes =) (Обычно для слов с пробелами)
            if is_on_gap:
                # Fix trouble when
                # Новая
                #      ^ + tab -> Новая         '   папка'
                # Теперь оно будет преобразовывать в Новая\ папка/ (если стоит в gap)

                unquoted_name = FS.normalize_name(name.removesuffix("'").removeprefix("'"),
                                                  quoting_type=QuotingType.ESCAPING_TYPE)
                return cls._cut_normalized_name_for_complete(
                    unquoted_name, being_completed=being_completed,
                    completion_scope=completion_scope)
            i = 0
        elif being_completed != completion_scope:  # if there is space between words (in one param)
            i = name.index(completion_scope, len(being_completed) - len(completion_scope))
        else:
            i = name.index(completion_scope)

        return name[i:]
