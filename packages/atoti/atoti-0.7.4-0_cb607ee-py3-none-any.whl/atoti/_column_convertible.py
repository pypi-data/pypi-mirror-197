from typing import Optional, Union

from atoti_core import (
    ComparisonOperator,
    Condition,
    ConditionBound,
    Constant,
    ConstantValue,
    HasCoordinates,
    Operation,
    OperationBound,
    is_constant_value,
)
from typing_extensions import TypeGuard

from ._column_coordinates import ColumnCoordinates

ColumnOperation = Operation[ColumnCoordinates]

# `isin` and combined conditions are not supported in UDAFs for now.
ColumnCondition = Condition[
    ColumnCoordinates,
    ComparisonOperator,
    Optional[Union[ColumnCoordinates, ColumnOperation, Constant]],
    None,
]

ColumnConditionOrOperation = Union[ColumnCondition, ColumnOperation]

NonConstantColumnConvertible = Union[
    ColumnConditionOrOperation,
    HasCoordinates[ColumnCoordinates],
]
ColumnConvertible = Union[
    ConstantValue,
    NonConstantColumnConvertible,
]


def _is_column_base_operation(value: Union[ConditionBound, OperationBound], /) -> bool:
    return value._coordinates_classes == frozenset([ColumnCoordinates])


def is_column_condition(value: object, /) -> TypeGuard[ColumnCondition]:
    return isinstance(value, Condition) and _is_column_base_operation(value)


def is_column_operation(value: object, /) -> TypeGuard[ColumnOperation]:
    return isinstance(value, Operation) and _is_column_base_operation(value)


def is_column_condition_or_operation(
    value: object, /
) -> TypeGuard[ColumnConditionOrOperation]:
    return (
        is_column_condition(value)
        if isinstance(value, Condition)
        else is_column_operation(value)
    )


def is_non_constant_column_convertible(
    value: object, /
) -> TypeGuard[NonConstantColumnConvertible]:
    return (
        isinstance(value._coordinates, ColumnCoordinates)
        if isinstance(value, HasCoordinates)
        else is_column_condition_or_operation(value)
    )


def is_column_convertible(value: object, /) -> TypeGuard[ColumnConvertible]:
    return (
        is_non_constant_column_convertible(value)
        if isinstance(value, (Condition, HasCoordinates, Operation))
        else is_constant_value(value)
    )
