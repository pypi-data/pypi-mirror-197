from __future__ import annotations

from atoti_core import doc

from .._docs_utils import STD_AND_VAR_DOC, VAR_DOC_KWARGS
from .._measure_convertible import NonConstantMeasureConvertible
from .._measure_description import MeasureDescription, convert_to_measure_description
from .._measures.calculated_measure import CalculatedMeasure, Operator
from .._runtime_type_checking_utils import VarianceMode
from ._utils import QUANTILE_STD_AND_VAR_DOC_KWARGS, check_array_type


@doc(STD_AND_VAR_DOC, **{**VAR_DOC_KWARGS, **QUANTILE_STD_AND_VAR_DOC_KWARGS})
def var(
    measure: NonConstantMeasureConvertible, /, *, mode: VarianceMode = "sample"
) -> MeasureDescription:
    check_array_type(measure)
    return CalculatedMeasure(
        Operator("variance", [convert_to_measure_description(measure), mode])
    )
