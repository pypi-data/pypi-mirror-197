from __future__ import annotations

from typing import Optional, Union, overload

from atoti_core import doc

from .._docs_utils import STD_AND_VAR_DOC, STD_DOC_KWARGS
from .._measure_convertible import NonConstantMeasureConvertible
from .._measure_description import MeasureDescription
from .._runtime_type_checking_utils import VarianceMode
from ..math import sqrt
from ..scope._scope import Scope
from ._utils import (
    QUANTILE_STD_AND_VAR_DOC_KWARGS,
    SCOPE_DOC,
    NonConstantColumnConvertibleOrLevel,
)
from .var import var


@overload
def std(
    operand: NonConstantColumnConvertibleOrLevel,
    /,
    *,
    mode: VarianceMode = "sample",
) -> MeasureDescription:
    ...


@overload
def std(
    operand: NonConstantMeasureConvertible,
    /,
    *,
    mode: VarianceMode = "sample",
    scope: Scope,
) -> MeasureDescription:
    ...


@doc(
    STD_AND_VAR_DOC,
    SCOPE_DOC,
    **{**STD_DOC_KWARGS, **QUANTILE_STD_AND_VAR_DOC_KWARGS},
)
def std(
    operand: Union[NonConstantColumnConvertibleOrLevel, NonConstantMeasureConvertible],
    /,
    *,
    mode: VarianceMode = "sample",
    scope: Optional[Scope] = None,
) -> MeasureDescription:
    return sqrt(
        # The type checkers cannot see that the `@overload` above ensure that this call is valid.
        var(operand, mode=mode, scope=scope),  # type: ignore
    )
