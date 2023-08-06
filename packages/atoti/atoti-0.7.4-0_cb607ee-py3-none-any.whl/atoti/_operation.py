from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING, Iterable, List, Optional, Sequence

from atoti_core import Constant, DataType, keyword_only_dataclass

from ._column_coordinates import ColumnCoordinates

if TYPE_CHECKING:
    from ._udaf_utils import (  # pylint: disable=nested-import
        JavaFunction,
        JavaOperationElement,
        OperationVisitor,
    )


def _get_new_columns(
    operation: Operation, column_names: Iterable[ColumnCoordinates]
) -> List[ColumnCoordinates]:
    columns: List[ColumnCoordinates] = []
    for column in operation.columns:
        if not column in column_names:
            columns.append(column)
    return columns


class Operation:
    """An operation between table columns."""

    @abstractmethod
    def accept(self, operation_visitor: OperationVisitor) -> JavaOperationElement:
        """Contribute this operation to the visitor."""

    @property
    @abstractmethod
    def columns(self) -> Sequence[ColumnCoordinates]:
        """Columns involved in this operation."""


class JavaFunctionOperation(Operation):
    @property
    @abstractmethod
    def underlyings(self) -> Sequence[Operation]:
        ...

    @property
    @abstractmethod
    def java_function(self) -> JavaFunction:
        ...

    def accept(self, operation_visitor: OperationVisitor) -> JavaOperationElement:
        return operation_visitor.visit_java_function_operation(self)

    @property
    def columns(self) -> Sequence[ColumnCoordinates]:
        columns: List[ColumnCoordinates] = []
        for underlying in self.underlyings:
            columns += _get_new_columns(underlying, columns)
        return columns


@dataclass(eq=False, frozen=True)
class ColumnOperation(Operation):  # pylint: disable=keyword-only-dataclass
    """Column of a table in an operation."""

    _column_coordinates: ColumnCoordinates
    _column_data_type: DataType

    def accept(self, operation_visitor: OperationVisitor) -> JavaOperationElement:
        return operation_visitor.visit_column_operation(operation=self)

    @property
    def columns(self) -> Sequence[ColumnCoordinates]:
        return [self._column_coordinates]


@dataclass(eq=False, frozen=True)
class ConstantOperation(Operation):  # pylint: disable=keyword-only-dataclass
    """Constant leaf of an operation."""

    _value: Constant

    def accept(self, operation_visitor: OperationVisitor) -> JavaOperationElement:
        return operation_visitor.visit_constant_operation(self)

    @property
    def columns(self) -> Sequence[ColumnCoordinates]:
        return []


@dataclass(eq=False, frozen=True)
class LeftRightOperation(
    JavaFunctionOperation
):  # pylint: disable=keyword-only-dataclass
    """Operation with left and right member."""

    _left: Operation
    _right: Operation

    @property
    def underlyings(self) -> Sequence[Operation]:
        return [self._left, self._right]


class MultiplicationOperation(LeftRightOperation):
    """Multiplication operation."""

    @property
    def java_function(self) -> JavaFunction:
        from ._udaf_utils import MUL_FUNCTION  # pylint: disable=nested-import

        return MUL_FUNCTION


class AdditionOperation(LeftRightOperation):
    """Addition operation."""

    @property
    def java_function(self) -> JavaFunction:
        from ._udaf_utils import ADD_FUNCTION  # pylint: disable=nested-import

        return ADD_FUNCTION


class SubtractionOperation(LeftRightOperation):
    """Subtraction operation."""

    @property
    def java_function(self) -> JavaFunction:
        from ._udaf_utils import SUB_FUNCTION  # pylint: disable=nested-import

        return SUB_FUNCTION


class DivisionOperation(LeftRightOperation):
    """Division operation."""

    @property
    def java_function(self) -> JavaFunction:
        from ._udaf_utils import TRUEDIV_FUNCTION  # pylint: disable=nested-import

        return TRUEDIV_FUNCTION


@keyword_only_dataclass
@dataclass(eq=False, frozen=True)
class TernaryOperation(Operation):
    condition: Operation
    true_operation: Operation
    false_operation: Optional[Operation]

    def accept(self, operation_visitor: OperationVisitor) -> JavaOperationElement:
        return operation_visitor.visit_ternary_operation(self)

    @property
    def columns(self) -> Sequence[ColumnCoordinates]:
        columns: List[ColumnCoordinates] = []
        columns += self.condition.columns
        columns += _get_new_columns(self.true_operation, columns)
        if self.false_operation is not None:
            columns += _get_new_columns(self.false_operation, columns)
        return columns


class ConditionOperation(LeftRightOperation):
    """Operations which can be used as conditions."""


class EqualOperation(ConditionOperation):
    """== operation."""

    @property
    def java_function(self) -> JavaFunction:
        from ._udaf_utils import EQ_FUNCTION  # pylint: disable=nested-import

        return EQ_FUNCTION


class NotEqualOperation(ConditionOperation):
    """!= operation."""

    @property
    def java_function(self) -> JavaFunction:
        from ._udaf_utils import NEQ_FUNCTION  # pylint: disable=nested-import

        return NEQ_FUNCTION


class GreaterThanOperation(ConditionOperation):
    """> operation."""

    @property
    def java_function(self) -> JavaFunction:
        from ._udaf_utils import GT_FUNCTION  # pylint: disable=nested-import

        return GT_FUNCTION


class GreaterThanOrEqualOperation(ConditionOperation):
    """>= operation."""

    @property
    def java_function(self) -> JavaFunction:
        from ._udaf_utils import GTE_FUNCTION  # pylint: disable=nested-import

        return GTE_FUNCTION


class LowerThanOperation(ConditionOperation):
    """< operation."""

    @property
    def java_function(self) -> JavaFunction:
        from ._udaf_utils import LT_FUNCTION  # pylint: disable=nested-import

        return LT_FUNCTION


class LowerThanOrEqualOperation(ConditionOperation):
    """<= operation."""

    @property
    def java_function(self) -> JavaFunction:
        from ._udaf_utils import LTE_FUNCTION  # pylint: disable=nested-import

        return LTE_FUNCTION
