from dataclasses import dataclass
from itertools import chain
from typing import FrozenSet, Optional, Type

from atoti_core import (
    Coordinates,
    CoordinatesT,
    Operand,
    OperandCondition,
    Operation,
    keyword_only_dataclass,
)


@keyword_only_dataclass
@dataclass(eq=False, frozen=True)
class WhereOperation(Operation[CoordinatesT]):
    condition: OperandCondition[CoordinatesT]
    true_value: Operand[CoordinatesT]
    false_value: Optional[Operand[CoordinatesT]]

    @property
    def _coordinates_classes(self) -> FrozenSet[Type[Coordinates]]:
        operands = [
            self.condition,
            self.true_value,
            self.false_value,
        ]
        return frozenset(
            chain(
                *(
                    self._get_coordinates_classes(
                        operand,
                    )
                    for operand in operands
                )
            )
        )
