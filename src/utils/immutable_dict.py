from collections.abc import Mapping
from typing import TypeVar

KT = TypeVar('KT')  # Key
VT = TypeVar('VT')  # Value


# https://docs.python.org/3/library/collections.abc.html
class ImmutableDict(Mapping[KT, VT]):
    def __init__(self, content: dict[KT, VT]):
        self._content = content

    def keys(self):
        return list(self._content)

    def __getitem__(self, key):
        return self._content[key]

    def __iter__(self):
        return iter(self._content)

    def __len__(self):
        return len(self._content)

    def __str__(self):
        return str(self._content)
