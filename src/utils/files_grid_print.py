import pathlib
import shutil

from math import ceil

from src.terminal.file_system.fs import fs
from src.utils.quoting_type import QuotingType


def files_grid_print(files: list[pathlib.Path]):
    if not files:
        return

    (terminal_width, _) = shutil.get_terminal_size()
    column_width = max([len(file.name) for file in files]) + 4

    columns_count = terminal_width // column_width
    if not columns_count:
        columns_count += 1

    rows_count = ceil(len(files) / columns_count)

    for row in range(rows_count):
        line_parts = []
        for col in range(columns_count):
            idx = row + col * rows_count
            if idx < len(files):
                file = files[idx]
                line_parts.append(f"{fs.normalize_name(name=file.name, quoting_type=QuotingType.ESCAPING_TYPE, path=file):<{column_width}}")

        if line_parts:
            print(''.join(line_parts))
