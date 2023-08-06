from __future__ import annotations

from abc import abstractmethod
from typing import Iterable, Iterator, MutableSet, Set, TypeVar

_Item = TypeVar("_Item")


class DelegateMutableSet(MutableSet[_Item]):
    @abstractmethod
    def _get_underlying(self) -> Set[_Item]:
        """Get the underlying set."""

    @abstractmethod
    def _set_underlying(self, new_set: Set[_Item], /) -> None:
        """Set the underlying set."""

    def __contains__(self, value: object, /) -> bool:
        return value in self._get_underlying()

    def __iter__(self) -> Iterator[_Item]:
        return iter(self._get_underlying())

    def __len__(self) -> int:
        return len(self._get_underlying())

    def __repr__(self) -> str:
        return repr(self._get_underlying())

    def add(self, value: _Item) -> None:
        new_set = set(self._get_underlying())
        new_set.add(value)
        self._set_underlying(new_set)

    def clear(self) -> None:
        new_set: Set[_Item] = set()
        self._set_underlying(new_set)

    def discard(self, value: _Item) -> None:
        new_set = set(self._get_underlying())
        new_set.discard(value)
        self._set_underlying(new_set)

    def update(self, *s: Iterable[_Item]) -> None:
        new_set = set(self._get_underlying())
        new_set.update(*s)
        self._set_underlying(new_set)
