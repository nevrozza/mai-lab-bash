import pathlib
import shutil

from math import ceil

from src.terminal.file_system.fs import fs
from src.utils.print_builder import PrintBuilder


def paths_grid_output(paths: list[pathlib.Path]) -> PrintBuilder:
    """
    Форматирует список путей в виде сетки для вывода в терминал
    :param paths: список путей
    :return: PrintBuilder
    """
    builder = PrintBuilder()
    if not paths:
        return builder

    (terminal_width, _) = shutil.get_terminal_size()
    column_width = max([len(file.name) for file in paths]) + 4

    columns_count = terminal_width // column_width
    if not columns_count:
        columns_count += 1

    rows_count = ceil(len(paths) / columns_count)

    for row in range(rows_count):
        line_parts = []
        for col in range(columns_count):
            idx = row + col * rows_count
            if idx < len(paths):
                file = paths[idx]
                line_parts.append(f"{fs.normalize_name(name=file.name, path=file):<{column_width}}")

        if line_parts:
            builder.append(''.join(line_parts))
    return builder
