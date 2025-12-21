import re
from collections.abc import Iterator
from pathlib import Path

from src.core.errors import BashError, BashNoSuchFileOrDirectoryError, BashCommandError
from src.terminal.command import BashCommand
from src.terminal.file_system.fs import fs
from src.terminal.file_system.resolve_path import resolve_path
from src.utils.print_builder import PrintBuilder


class GrepBashCommand(BashCommand):
    """Поиск строк по регулярному выражению в файлах"""

    @property
    def _supported_flags(self) -> str:
        return 'ri'

    @property
    def _max_params_count(self) -> int | None:
        return 2

    def _exec(self) -> tuple[list[BashError], str | None] | None:
        """Поиск шаблона в указанном файле или директории"""
        print_builder = PrintBuilder()

        pattern = self._params[0]
        path = resolve_path(self._params[1])

        recursive = 'r' in self._flags
        ignore_case = 'i' in self._flags

        flags = re.IGNORECASE if ignore_case else 0
        try:
            regex = re.compile(pattern, flags)
        except re.PatternError:
            raise BashCommandError(name=self.name(), msg=f"Invalid pattern '{pattern}'")

        files_to_search: Iterator[Path]
        if fs.properties.is_dir(path):
            if recursive:
                files_to_search = path.rglob("*")
            else:
                files_to_search = path.glob("*")
        else:
            files_to_search = iter([path])

        errors = []

        for file_path in files_to_search:
            search_errors, result = self._search_in_file(file_path, regex)
            if search_errors:
                errors.extend(search_errors)
            if result:
                print_builder.append(result)

        return errors, print_builder.get()

    def _search_in_file(self, file_path: Path, regex: re.Pattern) -> tuple[list[BashError], str]:
        """Ищет совпадения регулярного выражения по строкам файла"""
        print_builder = PrintBuilder()
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            lines = content.splitlines()

            for line_num, line in enumerate(lines, 1):
                match = regex.search(line)
                if match:
                    fragment = match.group(0)
                    print_builder.append(f"{file_path.name}:{line_num} {fragment}")

            return [], print_builder.get()
        except Exception as e:
            return [BashCommandError(name=self.name(), msg=f"Error reading file {file_path}: {str(e)}")], ""

    def _validate_params(self):
        """Проверяет наличие шаблона и корректность пути (при наличии)"""
        if len(self._params) == 0:
            raise BashCommandError(name=self.name(), msg="there is no pattern")
        elif len(self._params) == 1:
            self._params.append(fs.cwd_str())
        else:
            path = self._params[1]
            if not fs.properties.existing_path(path):
                raise BashNoSuchFileOrDirectoryError(name=self.name(), filename=path)
