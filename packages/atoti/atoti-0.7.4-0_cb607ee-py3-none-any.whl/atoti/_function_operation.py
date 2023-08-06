from dataclasses import dataclass
from itertools import chain
from typing import FrozenSet, Optional, Tuple, Type

from atoti_core import (
    Coordinates,
    CoordinatesT,
    Operand,
    Operation,
    keyword_only_dataclass,
)


@keyword_only_dataclass
@dataclass(eq=False, frozen=True)
class FunctionOperation(Operation[CoordinatesT]):
    function_key: str
    operands: Tuple[Optional[Operand[CoordinatesT]], ...] = ()

    @property
    def _coordinates_classes(self) -> FrozenSet[Type[Coordinates]]:
        return frozenset(
            chain(
                *(self._get_coordinates_classes(operand) for operand in self.operands)
            )
        )
