from __future__ import annotations

from functools import cached_property
from typing import Literal, Optional, Protocol, Sequence

from atoti_core import (
    Condition,
    Constant,
    ConstantValue,
    DataType,
    IsinCondition,
    OperandConvertibleWithCoordinates,
    ReprJson,
    ReprJsonable,
    is_json_primitive,
)
from typeguard import typeguard_ignore

from ._column_coordinates import ColumnCoordinates
from .type import DataType


class _GetColumnDataType(Protocol):
    def __call__(self, column_name: str, /, *, table_name: str) -> DataType:
        ...


class _GetColumnDefaultValue(Protocol):
    def __call__(self, column_name: str, /, *, table_name: str) -> Optional[Constant]:
        ...


class _SetColumnDefaultValue(Protocol):
    def __call__(
        self,
        default_value: Optional[Constant],
        /,
        *,
        column_name: str,
        table_name: str,
        data_type: DataType,
    ) -> None:
        ...


@typeguard_ignore
class Column(
    OperandConvertibleWithCoordinates[ColumnCoordinates],
    ReprJsonable,
):
    """Column of a :class:`atoti.Table`."""

    def __init__(
        self,
        name: str,
        /,
        *,
        get_column_data_type: _GetColumnDataType,
        get_column_default_value: _GetColumnDefaultValue,
        set_column_default_value: _SetColumnDefaultValue,
        table_keys: Sequence[str],
        table_name: str,
    ) -> None:
        super().__init__()

        self._name = name
        self._table_keys = table_keys
        self._table_name = table_name
        self._get_column_data_type = get_column_data_type
        self._get_column_default_value = get_column_default_value
        self._set_column_default_value = set_column_default_value

    @property
    def name(self) -> str:
        """The name of the column."""
        return self._name

    @cached_property
    def data_type(self) -> DataType:
        """The type of the elements in the column."""
        return self._get_column_data_type(self.name, table_name=self._table_name)

    @property
    def _coordinates(self) -> ColumnCoordinates:
        return ColumnCoordinates(table_name=self._table_name, column_name=self.name)

    @property
    def _operation_operand(self) -> ColumnCoordinates:
        return self._coordinates

    @property
    def default_value(self) -> Optional[ConstantValue]:
        """Value used to replace ``None`` inserted values.

        Each data type has its own default ``default_value`` value:

        >>> from pprint import pprint
        >>> table = session.create_table(
        ...     "Main data types",
        ...     types={
        ...         "boolean": tt.BOOLEAN,
        ...         "double": tt.DOUBLE,
        ...         "double[]": tt.DOUBLE_ARRAY,
        ...         "float": tt.FLOAT,
        ...         "float[]": tt.FLOAT_ARRAY,
        ...         "int": tt.INT,
        ...         "int[]": tt.INT_ARRAY,
        ...         "LocalDate": tt.LOCAL_DATE,
        ...         "LocalDateTime": tt.LOCAL_DATE_TIME,
        ...         "LocalTime": tt.LOCAL_TIME,
        ...         "long": tt.LONG,
        ...         "long[]": tt.LONG_ARRAY,
        ...         "String": tt.STRING,
        ...         "ZonedDateTime": tt.ZONED_DATE_TIME,
        ...     },
        ... )
        >>> pprint(
        ...     {
        ...         column_name: table[column_name].default_value
        ...         for column_name in table.columns
        ...     },
        ...     sort_dicts=False,
        ... )
        {'boolean': False,
         'double': None,
         'double[]': None,
         'float': None,
         'float[]': None,
         'int': None,
         'int[]': None,
         'LocalDate': datetime.date(1970, 1, 1),
         'LocalDateTime': datetime.datetime(1970, 1, 1, 0, 0),
         'LocalTime': datetime.time(0, 0),
         'long': None,
         'long[]': None,
         'String': 'N/A',
         'ZonedDateTime': datetime.datetime(1970, 1, 1, 0, 0, tzinfo=tzutc())}

        Key columns cannot have ``None`` as their default value so it is forced to something else.
        For numeric scalar columns, this is zero:

        >>> table = session.create_table(
        ...     "Numeric",
        ...     keys=["int", "float"],
        ...     types={
        ...         "int": tt.INT,
        ...         "float": tt.FLOAT,
        ...         "long": tt.LONG,
        ...         "double": tt.DOUBLE,
        ...     },
        ... )
        >>> {
        ...     column_name: table[column_name].default_value
        ...     for column_name in table.columns
        ... }
        {'int': 0, 'float': 0.0, 'long': None, 'double': None}
        >>> table += (None, None, None, None)
        >>> table.head()
                   long  double
        int float
        0   0.0     NaN     NaN

        The default value of array columns is ``None`` and cannot be changed:

        >>> session.create_table(  # doctest: +ELLIPSIS
        ...     "Array",
        ...     types={"long array": tt.LONG_ARRAY},
        ...     default_values={"long array": [0, 0]},
        ... )
        Traceback (most recent call last):
            ...
        atoti._exceptions.AtotiJavaException: Cannot make an array type non-nullable. ...

        Changing the default value from ``None`` to something else affects both the previously inserted ``None`` values and the upcoming ones:

        >>> table["long"].default_value = 42
        >>> table["long"].default_value
        42
        >>> table.head()
                   long  double
        int float
        0   0.0      42     NaN
        >>> table += (1, None, None, None)
        >>> table.head()
                   long  double
        int float
        0   0.0      42     NaN
        1   0.0      42     NaN

        Once a column has a default value different than ``None``, it cannot be changed anymore:

        >>> table["long"].default_value = 1337
        Traceback (most recent call last):
            ...
        NotImplementedError: The default value is already not ``None`` and cannot be changed: recreate the table using the `default_values` parameter instead.
        >>> table["long"].default_value
        42
        >>> del session.tables["Numeric"]
        >>> table = session.create_table(
        ...     "Numeric",
        ...     keys=["int", "float"],
        ...     types={
        ...         "int": tt.INT,
        ...         "float": tt.FLOAT,
        ...         "long": tt.LONG,
        ...         "double": tt.DOUBLE,
        ...     },
        ...     default_values={"long": 1337},
        ... )
        >>> table["long"].default_value
        1337

        The default value can also not be changed to ``None``:

        >>> table = session.create_table("Stringly", types={"String": tt.STRING})
        >>> table["String"].default_value = None
        Traceback (most recent call last):
            ...
        NotImplementedError: The default value cannot be changed to `None`: recreate the table using the `default_values` parameter instead.
        >>> table["String"].default_value
        'N/A'
        >>> del session.tables["Stringly"]
        >>> table = session.create_table(
        ...     "Stringly",
        ...     types={"String": tt.STRING},
        ...     default_values={"String": None},
        ... )
        >>> print(table["String"].default_value)
        None
        """
        default_value = self._get_column_default_value(
            self.name, table_name=self._table_name
        )
        return None if default_value is None else default_value.value

    @default_value.setter
    def default_value(self, default_value: Optional[ConstantValue]) -> None:
        alternative = "recreate the table using the `default_values` parameter instead"
        if default_value is None:
            raise NotImplementedError(
                f"The default value cannot be changed to `None`: {alternative}."
            )
        if self.default_value is not None:
            # See https://support.activeviam.com/jira/browse/PIVOT-5681.
            raise NotImplementedError(
                f"The default value is already not ``None`` and cannot be changed: {alternative}."
            )
        self._set_column_default_value(
            None if default_value is None else Constant(default_value),
            column_name=self.name,
            table_name=self._table_name,
            data_type=self.data_type,
        )

    def isin(
        self, *elements: Optional[ConstantValue]
    ) -> Condition[ColumnCoordinates, Literal["isin"], Optional[Constant], None]:
        """Return a condition evaluating to ``True`` if a column element is among the given elements and ``False`` otherwise.

        ``table["City"].isin("Paris", "New York")`` is equivalent to ``(table["City"] == "Paris") | (table["City"] == "New York")``.

        Args:
            elements: One or more elements on which the column should be."""
        return IsinCondition(
            subject=self._operation_operand,
            elements=tuple(
                None if element is None else Constant(element) for element in elements
            ),
        )

    def _repr_json_(self) -> ReprJson:
        return {
            "key": self.name in self._table_keys,
            "type": self.data_type,
            "default_value": self.default_value
            if is_json_primitive(self.default_value)
            else repr(self.default_value),
        }, {"expanded": True, "root": self.name}
