from dataclasses import dataclass
from typing import Optional

from atoti_core import keyword_only_dataclass

from .._column_coordinates import ColumnCoordinates
from .._java_api import JavaApi
from .._measure_description import MeasureDescription
from .._measure_metadata import MeasureMetadata


@keyword_only_dataclass
@dataclass(eq=False, frozen=True)
class ColumnMeasure(MeasureDescription):
    """Measure based on the column of a table."""

    _column_coordinates: ColumnCoordinates
    _plugin_key: str

    def _do_distil(
        self,
        *,
        java_api: JavaApi,
        cube_name: str,
        measure_name: Optional[str] = None,
        measure_metadata: Optional[MeasureMetadata] = None,
    ) -> str:
        return java_api.aggregated_measure(
            cube_name=cube_name,
            measure_name=measure_name,
            table_name=self._column_coordinates.table_name,
            column_name=self._column_coordinates.column_name,
            agg_function=self._plugin_key,
            measure_metadata=measure_metadata,
        )
