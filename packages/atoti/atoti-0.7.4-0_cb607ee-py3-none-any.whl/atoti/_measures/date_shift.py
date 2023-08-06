from dataclasses import dataclass
from typing import Optional

from atoti_core import LevelCoordinates, keyword_only_dataclass

from .._java_api import JavaApi
from .._measure_description import MeasureDescription
from .._measure_metadata import MeasureMetadata
from .utils import get_measure_name


@keyword_only_dataclass
@dataclass(eq=False, frozen=True)
class DateShift(MeasureDescription):
    """Shift the value."""

    _underlying_measure: MeasureDescription
    _level_coordinates: LevelCoordinates
    _shift: str
    _method: str

    def _do_distil(
        self,
        *,
        java_api: JavaApi,
        cube_name: str,
        measure_name: Optional[str] = None,
        measure_metadata: Optional[MeasureMetadata] = None,
    ) -> str:
        underlying_name = get_measure_name(
            java_api=java_api, measure=self._underlying_measure, cube_name=cube_name
        )
        distilled_name = java_api.create_measure(
            cube_name,
            measure_name,
            "DATE_SHIFT",
            underlying_name,
            self._level_coordinates.java_description,
            self._shift,
            self._method,
            measure_metadata=measure_metadata,
        )
        return distilled_name
