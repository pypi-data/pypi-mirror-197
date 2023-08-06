from typing import Iterable, Optional

from atoti_core import deprecated

from .._measure_description import MeasureDescription
from ..agg import single_value
from ..column import Column
from ..level import Level


def value(
    column: Column, *, levels: Optional[Iterable[Level]] = None
) -> MeasureDescription:

    assert (
        not levels
    ), "Levels are no longer supported. Use `where()` to restrict the visibility of the measure."

    deprecated("`value()` has been deprecated. Use `agg.single_value()` instead.")
    return single_value(column)
