from dataclasses import dataclass
from typing import Optional, Sequence

from atoti_core import is_array_type, keyword_only_dataclass

from .._java_api import JavaApi
from .._measure_convertible import MeasureConvertible
from .._measure_description import MeasureDescription, convert_to_measure_description
from .._measure_metadata import MeasureMetadata
from ..column import Column
from ..type import DOUBLE_ARRAY
from .utils import convert_measure_args


@keyword_only_dataclass
@dataclass(eq=False, frozen=True)
class SumProductFieldsMeasure(MeasureDescription):
    """Sum of the product of factors for table fields."""

    _factors: Sequence[Column]

    def _do_distil(
        self,
        *,
        java_api: JavaApi,
        cube_name: str,
        measure_name: Optional[str] = None,
        measure_metadata: Optional[MeasureMetadata] = None,
    ) -> str:
        # Checks fields are in the selection, otherwise use the other sum product implementation because UDAF needs fields in the selection.
        selection_fields = java_api.get_selection_fields(cube_name)
        if not all(factor._coordinates in selection_fields for factor in self._factors):
            raise ValueError(
                f"The columns {[factor.name for factor in self._factors if not factor._coordinates in selection_fields]}"
                f" cannot be used in a sum product aggregation without first being converted into measures."
            )
        factors_and_type = {}
        for factor in self._factors:
            if is_array_type(factor.data_type) and factor.data_type != DOUBLE_ARRAY:
                raise TypeError(
                    f"Only array columns of type `{DOUBLE_ARRAY}` are supported and `{repr(factor._coordinates)}` is not."
                )
            factors_and_type[factor._coordinates] = factor.data_type
        return java_api.create_measure(
            cube_name,
            measure_name,
            "SUM_PRODUCT_UDAF",
            [factor._coordinates for factor in self._factors],
            factors_and_type,
            measure_metadata=measure_metadata,
        )


@keyword_only_dataclass
@dataclass(eq=False, frozen=True)
class SumProductEncapsulationMeasure(MeasureDescription):
    """Create an intermediate measure needing to be aggregated with the key "ATOTI_SUM_PRODUCT"."""

    _factors: Sequence[MeasureConvertible]

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
            "SUM_PRODUCT_ENCAPSULATION",
            convert_measure_args(
                java_api=java_api,
                cube_name=cube_name,
                args=tuple(
                    convert_to_measure_description(factor) for factor in self._factors
                ),
            ),
            measure_metadata=measure_metadata,
        )
