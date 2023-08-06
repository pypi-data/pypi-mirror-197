from __future__ import annotations

from typing import Tuple, Union

from typing_extensions import TypeGuard

from ._measure_convertible import MeasureConvertible, is_measure_convertible
from ._measure_metadata import MeasureMetadata

MeasureDefinition = Union[
    MeasureConvertible, Tuple[MeasureConvertible, MeasureMetadata]
]


def _is_measure_convertible_with_metadata(
    measure_definition: MeasureDefinition, /
) -> TypeGuard[Tuple[MeasureConvertible, MeasureMetadata]]:
    return (
        isinstance(measure_definition, tuple)
        and len(measure_definition) == 2
        and isinstance(measure_definition[1], MeasureMetadata)
    )


def get_measure_convertible_and_metadata(
    measure_definition: MeasureDefinition, /
) -> Tuple[MeasureConvertible, MeasureMetadata]:
    if _is_measure_convertible_with_metadata(measure_definition):
        return measure_definition
    assert is_measure_convertible(measure_definition)
    return measure_definition, MeasureMetadata()
