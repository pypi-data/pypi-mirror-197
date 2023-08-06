from __future__ import annotations

from typing import Optional, Union

from atoti_core import (
    Condition,
    ConditionBound,
    ConditionCombinationOperatorBound,
    ConditionComparisonOperatorBound,
    Constant,
    ConstantValue,
    HasCoordinates,
    HierarchyCoordinates,
    LevelCoordinates,
    MeasureCoordinates,
    Operation,
    OperationBound,
    is_constant_value,
)
from typing_extensions import TypeGuard

MeasureConvertibleCoordinates = Union[LevelCoordinates, MeasureCoordinates]

MeasureOperation = Operation[MeasureConvertibleCoordinates]

MeasureCondition = Condition[
    Union[HierarchyCoordinates, MeasureConvertibleCoordinates, MeasureOperation],
    ConditionComparisonOperatorBound,
    Optional[
        Union[
            Constant,
            MeasureConvertibleCoordinates,
            MeasureOperation,
        ]
    ],
    ConditionCombinationOperatorBound,
]


MeasureConditionOrOperation = Union[MeasureCondition, MeasureOperation]

NonConstantMeasureOperand = Union[
    MeasureConditionOrOperation, MeasureConvertibleCoordinates
]
MeasureOperand = Union[Constant, NonConstantMeasureOperand]

NonConstantMeasureConvertible = Union[
    HasCoordinates[MeasureConvertibleCoordinates], MeasureConditionOrOperation
]

MeasureConvertible = Union[ConstantValue, NonConstantMeasureConvertible]


def _is_measure_base_operation(value: Union[ConditionBound, OperationBound], /) -> bool:
    # It is not a measure `BaseOperation` if there are some unexpected coordinates classes.
    return not (
        value._coordinates_classes
        - {HierarchyCoordinates, LevelCoordinates, MeasureCoordinates}
    )


def is_measure_condition(value: object, /) -> TypeGuard[MeasureCondition]:
    return isinstance(value, Condition) and _is_measure_base_operation(value)


def is_measure_operation(value: object, /) -> TypeGuard[MeasureOperation]:
    return isinstance(value, Operation) and _is_measure_base_operation(value)


def is_measure_condition_or_operation(
    value: object, /
) -> TypeGuard[MeasureConditionOrOperation]:
    return (
        is_measure_condition(value)
        if isinstance(value, Condition)
        else is_measure_operation(value)
    )


def is_non_constant_measure_convertible(
    value: object, /
) -> TypeGuard[NonConstantMeasureConvertible]:
    return (
        isinstance(
            value._coordinates,
            (HierarchyCoordinates, LevelCoordinates, MeasureCoordinates),
        )
        if isinstance(value, HasCoordinates)
        else is_measure_condition_or_operation(value)
    )


def is_measure_convertible(value: object, /) -> TypeGuard[MeasureConvertible]:
    return (
        is_non_constant_measure_convertible(value)
        if isinstance(value, (Condition, HasCoordinates, Operation))
        else is_constant_value(value)
    )
