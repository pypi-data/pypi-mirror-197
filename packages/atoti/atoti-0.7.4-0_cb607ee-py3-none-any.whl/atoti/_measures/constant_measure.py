from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from atoti_core import Constant, keyword_only_dataclass

from .._java_api import JavaApi
from .._measure_description import MeasureDescription
from .._measure_metadata import MeasureMetadata
from .._py4j_utils import as_java_object


@keyword_only_dataclass
@dataclass(eq=False, frozen=True)
class ConstantMeasure(MeasureDescription):
    """A measure equal to a constant."""

    _value: Constant

    def _do_distil(
        self,
        *,
        java_api: JavaApi,
        cube_name: str,
        measure_name: Optional[str] = None,
        measure_metadata: Optional[MeasureMetadata] = None,
    ) -> str:
        value = as_java_object(self._value.value, gateway=java_api.gateway)
        distilled_name = java_api.create_measure(
            cube_name,
            measure_name,
            "CONSTANT",
            value,
            measure_metadata=measure_metadata,
        )
        return distilled_name
