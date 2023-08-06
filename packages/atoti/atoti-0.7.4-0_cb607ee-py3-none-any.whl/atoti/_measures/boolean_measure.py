from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple

from .._java_api import JavaApi
from .._measure_description import MeasureDescription
from .._measure_metadata import MeasureMetadata
from .utils import convert_measure_args


@dataclass(eq=False, frozen=True)
class BooleanMeasure(MeasureDescription):  # pylint: disable=keyword-only-dataclass
    """Boolean operation between measures."""

    _operator: str
    _operands: Tuple[MeasureDescription, ...]

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
            "BOOLEAN",
            self._operator,
            convert_measure_args(
                java_api=java_api, cube_name=cube_name, args=self._operands
            ),
            measure_metadata=measure_metadata,
        )
