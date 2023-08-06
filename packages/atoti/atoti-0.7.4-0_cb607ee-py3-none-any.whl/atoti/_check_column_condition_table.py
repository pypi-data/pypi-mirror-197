from itertools import chain
from typing import Literal

from atoti_core import (
    ComparisonCondition,
    Condition,
    ConditionCombinationOperatorBound,
    ConditionComparisonOperatorBound,
    ConditionTargetBound,
    decombine_condition,
)

from ._column_coordinates import ColumnCoordinates


def check_column_condition_table(
    condition: Condition[
        ColumnCoordinates,
        ConditionComparisonOperatorBound,
        ConditionTargetBound,
        ConditionCombinationOperatorBound,
    ],
    /,
    *,
    attribute_name: Literal["subject", "target"],
    expected_table_name: str,
) -> None:
    error_message_template = f"Expected the {{attribute_name}} of the condition to belong to the table `{expected_table_name}` but got `{{table_name}}`."

    for decombined_conditions in decombine_condition(  # type: ignore[var-annotated]
        condition, allowed_subject_types=(ColumnCoordinates,)
    ):
        for sub_condition in chain(*decombined_conditions):
            if attribute_name == "subject":
                # Pyright is able to check that `sub_condition` has a `subject` but mypy cannot.
                table_name = sub_condition.subject.table_name  # type: ignore[attr-defined]
                if table_name != expected_table_name:
                    raise ValueError(
                        error_message_template.format(
                            attribute_name=attribute_name, table_name=table_name
                        )
                    )
            elif attribute_name == "target":
                assert isinstance(sub_condition, ComparisonCondition)
                assert isinstance(sub_condition.target, ColumnCoordinates)
                table_name = sub_condition.target.table_name
                if table_name != expected_table_name:
                    raise ValueError(
                        error_message_template.format(
                            attribute_name=attribute_name, table_name=table_name
                        )
                    )
