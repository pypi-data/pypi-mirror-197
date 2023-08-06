from typing import Collection, Dict, Literal, Mapping, Optional, Tuple

from atoti_core import (
    ComparisonCondition,
    Condition,
    Constant,
    IsinCondition,
    LevelCoordinates,
    combine_conditions,
    decombine_condition,
)

JavaFilters = Mapping[LevelCoordinates, Tuple[Constant, ...]]

AggregateProviderFilter = Condition[
    LevelCoordinates, Literal["eq", "isin"], Constant, Optional[Literal["and"]]
]


def to_java_filters(condition: AggregateProviderFilter, /) -> JavaFilters:
    filters: Dict[LevelCoordinates, Tuple[Constant, ...]] = {}

    comparison_conditions, isin_conditions, _ = decombine_condition(
        condition,
        allowed_subject_types=(LevelCoordinates,),
        allowed_comparison_operators=("eq",),
        allowed_target_types=(Constant,),
        allowed_combination_operators=("and",),
        allowed_isin_element_types=(Constant,),
    )[0]

    for comparison_condition in comparison_conditions:
        filters[comparison_condition.subject] = (comparison_condition.target,)

    for isin_condition in isin_conditions:
        filters[isin_condition.subject] = isin_condition.elements

    return filters


def to_python_condition(filters: JavaFilters, /) -> Optional[AggregateProviderFilter]:
    if not filters:
        return None

    conditions: Collection[AggregateProviderFilter] = [
        # Pyright is able to check the type of the conditions but mypy cannot.
        ComparisonCondition(subject=level_coordinates, operator="eq", target=values[0])  # type: ignore[misc]
        if len(values) == 0
        else IsinCondition(subject=level_coordinates, elements=values)
        for level_coordinates, values in filters.items()
    ]
    return combine_conditions((conditions,))
