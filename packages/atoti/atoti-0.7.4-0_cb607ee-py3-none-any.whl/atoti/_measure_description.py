from __future__ import annotations

import math
from abc import abstractmethod
from dataclasses import dataclass
from typing import FrozenSet, Optional, Type, cast

from atoti_core import (
    ArithmeticOperation,
    CombinedCondition,
    ComparisonCondition,
    Condition,
    Constant,
    Coordinates,
    HasCoordinates,
    HierarchyCoordinates,
    HierarchyIsinCondition,
    IndexingOperation,
    IsinCondition,
    LevelCoordinates,
    MeasureCoordinates,
    Operation,
    keyword_only_dataclass,
)
from typeguard import typeguard_ignore

from ._java_api import JavaApi
from ._measure_convertible import MeasureConvertible, MeasureOperand
from ._measure_metadata import MeasureMetadata


@keyword_only_dataclass
@typeguard_ignore
@dataclass(eq=False, frozen=True)
class MeasureDescription(Operation[MeasureCoordinates]):
    """The description of a :class:`~atoti.Measure` that has not been added to the cube yet."""

    def _distil(
        self,
        *,
        java_api: JavaApi,
        cube_name: str,
        measure_name: Optional[str] = None,
        measure_metadata: Optional[MeasureMetadata] = None,
    ) -> str:
        """Return the name of the measure, creating it in the cube if it does not exist yet."""
        name: Optional[str] = self.__dict__.get("_name")
        if not name:
            name = self._do_distil(  # pylint: disable=attribute-defined-outside-init
                java_api=java_api,
                cube_name=cube_name,
                measure_name=measure_name,
                measure_metadata=measure_metadata,
            )
            self.__dict__["_name"] = name
        elif measure_name is not None:
            # This measure has already been distilled, this is a copy with a different name.
            java_api.copy_measure(
                name,
                measure_name,
                cube_name=cube_name,
                measure_metadata=measure_metadata,
            )
        return name

    @abstractmethod
    def _do_distil(
        self,
        *,
        java_api: JavaApi,
        cube_name: str,
        measure_name: Optional[str] = None,
        measure_metadata: Optional[MeasureMetadata] = None,
    ) -> str:
        """Create the measure in the cube and return its name."""

    @property
    def _coordinates_classes(self) -> FrozenSet[Type[Coordinates]]:
        return frozenset([MeasureCoordinates])


def convert_operand_to_measure_description(
    value: Optional[MeasureOperand], /
) -> MeasureDescription:
    # pylint: disable=nested-import
    from ._measures.level_measure import LevelMeasure
    from ._measures.published_measure import PublishedMeasure

    # pylint: enable=nested-import

    if value is None:
        raise TypeError(
            f"Cannot convert `{value}` operand to `{MeasureDescription.__name__}`."
        )

    if isinstance(value, LevelCoordinates):
        return LevelMeasure(value)

    if isinstance(value, MeasureCoordinates):
        return PublishedMeasure(value.measure_name)

    return convert_to_measure_description(
        value.value if isinstance(value, Constant) else cast(MeasureConvertible, value)
    )


def convert_to_measure_description(  # pylint: disable=too-many-branches,too-many-return-statements
    value: MeasureConvertible, /
) -> MeasureDescription:
    # pylint: disable=nested-import
    from ._measures.boolean_measure import BooleanMeasure
    from ._measures.calculated_measure import CalculatedMeasure, Operator
    from ._measures.constant_measure import ConstantMeasure
    from ._measures.level_measure import LevelMeasure
    from ._measures.published_measure import PublishedMeasure

    # pylint: enable=nested-import

    if isinstance(value, MeasureDescription):
        return value

    if isinstance(value, Condition):
        if isinstance(value, CombinedCondition):
            return BooleanMeasure(
                value.boolean_operator,
                tuple(
                    convert_to_measure_description(operand)
                    for operand in value.sub_conditions
                ),
            )

        if isinstance(value, ComparisonCondition):
            assert not isinstance(
                value.subject, HierarchyCoordinates
            ), f"Instances of `{HierarchyIsinCondition.__name__}` should have been converted to combined `{ComparisonCondition.__name__}`s."

            subject = convert_operand_to_measure_description(value.subject)
            if value.target is None:
                return BooleanMeasure(
                    "isNull" if value.operator == "eq" else "notNull",
                    (subject,),
                )
            return BooleanMeasure(
                value.operator,
                (
                    subject,
                    convert_operand_to_measure_description(value.target),
                ),
            )

        if isinstance(value, (HierarchyIsinCondition, IsinCondition)):
            return convert_to_measure_description(value.combined_comparison_condition)

        raise TypeError(f"Unexpected condition type: `{type(value)}`.")

    if isinstance(value, HasCoordinates):
        coordinates = value._coordinates

        return (
            PublishedMeasure(coordinates.measure_name)
            if isinstance(coordinates, MeasureCoordinates)
            else LevelMeasure(coordinates)
        )

    if isinstance(value, Operation):
        if isinstance(value, ArithmeticOperation):
            return CalculatedMeasure(
                Operator(
                    value.operator,
                    [
                        convert_operand_to_measure_description(operand)
                        for operand in value.operands
                    ],
                )
            )

        if isinstance(value, IndexingOperation):
            if isinstance(value.index, slice):
                if value.index.step:
                    raise ValueError(
                        "Cannot index an array measure using a slice with a step."
                    )
                start = value.index.start if value.index.start is not None else 0
                stop = value.index.stop if value.index.stop is not None else math.inf
                return CalculatedMeasure(
                    Operator(
                        "vector_sub",
                        [
                            convert_operand_to_measure_description(value.operand),
                            convert_to_measure_description(start),
                            convert_to_measure_description(stop),
                        ],
                    )
                )

            return CalculatedMeasure(
                Operator(
                    "vector_element",
                    [
                        convert_operand_to_measure_description(value.operand),
                        convert_operand_to_measure_description(value.index),
                    ],
                )
            )

        raise TypeError(f"Unexpected operation type: `{type(value)}`.")

    return ConstantMeasure(
        _value=Constant(
            # Tuples are not valid constants, lists are.
            # See comment explaining why in `atoti_core.constant`.
            list(value)
            if isinstance(value, tuple)
            else value
        ),
    )
