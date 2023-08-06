from __future__ import annotations

from atoti_core import doc

from .._docs_utils import QUANTILE_DOC
from .._measure_convertible import MeasureConvertible, NonConstantMeasureConvertible
from .._measure_description import MeasureDescription, convert_to_measure_description
from .._measures.generic_measure import GenericMeasure
from .._runtime_type_checking_utils import PercentileInterpolation, PercentileMode
from ._utils import QUANTILE_STD_AND_VAR_DOC_KWARGS, check_array_type


@doc(QUANTILE_DOC, **QUANTILE_STD_AND_VAR_DOC_KWARGS)
def quantile(
    measure: NonConstantMeasureConvertible,
    /,
    q: MeasureConvertible,
    *,
    mode: PercentileMode = "inc",
    interpolation: PercentileInterpolation = "linear",
) -> MeasureDescription:
    if isinstance(q, float):
        if q < 0 or q > 1:
            raise ValueError("Quantile must be between 0 and 1.")
    check_array_type(measure)
    return GenericMeasure(
        "CALCULATED_QUANTILE",
        mode,
        interpolation,
        [convert_to_measure_description(arg) for arg in [measure, q]],
    )
