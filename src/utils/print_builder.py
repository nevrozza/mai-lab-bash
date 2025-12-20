class PrintBuilder:

    def __init__(self):
        self.lines: list[str] = []

    def append(self, to_append: str | PrintBuilder):
        if isinstance(to_append, PrintBuilder):
            self.lines += to_append.lines
        else:
            self.lines.append(to_append)

    def get(self) -> str:
        return "\n".join(self.lines)
