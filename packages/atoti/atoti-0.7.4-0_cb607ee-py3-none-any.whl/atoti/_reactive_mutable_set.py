from __future__ import annotations

from abc import abstractmethod
from typing import Iterable, Iterator, MutableSet, TypeVar

_Item = TypeVar("_Item")


class ReactiveMutableSet(MutableSet[_Item]):
    def __init__(self, data: Iterable[_Item], /) -> None:
        super().__init__()

        self._data = set(data)

    @abstractmethod
    def _on_change(self) -> None:
        """Hook called each time the data in the set changes."""

    def __contains__(self, value: object) -> bool:
        return value in self._data

    def add(self, value: _Item) -> None:
        self._data.add(value)
        self._on_change()

    def clear(self) -> None:
        self._data.clear()
        self._on_change()

    def discard(self, value: _Item) -> None:
        self._data.discard(value)
        self._on_change()

    def update(self, *s: Iterable[_Item]) -> None:
        self._data.update(*s)
        self._on_change()

    def __iter__(self) -> Iterator[_Item]:
        return iter(self._data)

    def __len__(self) -> int:
        return len(self._data)

    def __repr__(self) -> str:
        return repr(self._data)
