from __future__ import annotations

from typing import Optional, Union, overload

from atoti_core import doc

from .._measure_convertible import NonConstantMeasureConvertible
from .._measure_description import MeasureDescription
from ..scope._scope import Scope
from ._agg import agg
from ._utils import BASIC_ARGS_DOC, BASIC_DOC, NonConstantColumnConvertibleOrLevel


@overload
def max(  # pylint: disable=redefined-builtin
    operand: NonConstantColumnConvertibleOrLevel, /
) -> MeasureDescription:
    ...


@overload
def max(  # pylint: disable=redefined-builtin
    operand: NonConstantMeasureConvertible, /, *, scope: Scope
) -> MeasureDescription:
    ...


@doc(
    BASIC_DOC,
    args=BASIC_ARGS_DOC,
    value="maximum",
    example="""
        >>> m["Maximum Price"] = tt.agg.max(table["Price"])
        >>> cube.query(m["Maximum Price"])
          Maximum Price
        0         43.00""".replace(
        "\n", "", 1
    ),
)
def max(  # pylint: disable=redefined-builtin
    operand: Union[NonConstantColumnConvertibleOrLevel, NonConstantMeasureConvertible],
    /,
    *,
    scope: Optional[Scope] = None,
) -> MeasureDescription:
    # The type checkers cannot see that the `@overload` above ensure that this call is valid.
    return agg(operand, plugin_key="MAX", scope=scope)  # type: ignore
