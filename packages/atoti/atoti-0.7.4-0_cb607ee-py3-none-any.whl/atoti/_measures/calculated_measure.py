from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Optional, Sequence, Union

from atoti_core import LevelCoordinates, keyword_only_dataclass

from .._java_api import JavaApi
from .._measure_convertible import NonConstantMeasureConvertible
from .._measure_description import MeasureDescription
from .._measure_metadata import MeasureMetadata
from .utils import convert_measure_args

_Operand = Union[MeasureDescription, str]


@dataclass(frozen=True)
class Operator:  # pylint: disable=keyword-only-dataclass
    """An operator to create a calculated measure from other measures."""

    _name: str
    _operands: Sequence[_Operand]


@dataclass(eq=False, frozen=True)
class CalculatedMeasure(MeasureDescription):  # pylint: disable=keyword-only-dataclass
    """A calculated measure is the result of an operation between other measures."""

    _operator: Operator

    def _do_distil(
        self,
        *,
        java_api: JavaApi,
        cube_name: str,
        measure_name: Optional[str] = None,
        measure_metadata: Optional[MeasureMetadata] = None,
    ) -> str:
        return java_api.create_measure(
            cube_name,
            measure_name,
            "CALCULATED",
            self._operator._name,
            convert_measure_args(
                java_api=java_api,
                cube_name=cube_name,
                args=self._operator._operands,
            ),
            measure_metadata=measure_metadata,
        )


@keyword_only_dataclass
@dataclass(eq=False, frozen=True)
class AggregatedMeasure(MeasureDescription):
    """Aggregated measure."""

    _underlying_measure: NonConstantMeasureConvertible
    _plugin_key: str
    _on_levels: Iterable[LevelCoordinates] = ()

    def _do_distil(
        self,
        *,
        java_api: JavaApi,
        cube_name: str,
        measure_name: Optional[str] = None,
        measure_metadata: Optional[MeasureMetadata] = None,
    ) -> str:
        distilled_name = java_api.create_measure(
            cube_name,
            measure_name,
            "LEAF_AGGREGATION",
            *convert_measure_args(
                java_api=java_api, cube_name=cube_name, args=(self._underlying_measure,)
            ),
            [
                level_coordinates.java_description
                for level_coordinates in self._on_levels
            ],
            self._plugin_key,
            measure_metadata=measure_metadata,
        )
        return distilled_name
