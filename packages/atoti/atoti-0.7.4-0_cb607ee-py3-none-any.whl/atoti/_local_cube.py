from __future__ import annotations

from abc import abstractmethod
from datetime import timedelta
from typing import Any, Callable, Dict, Iterable, Literal, Optional, TypeVar

import pandas as pd
from atoti_core import (
    BASE_SCENARIO_NAME,
    EMPTY_MAPPING,
    QUERY_DOC,
    BaseCube,
    BaseHierarchyBound,
    BaseLevel,
    BaseMeasure,
    Context,
    DataType,
    LevelCoordinates,
    LevelsT,
    QueryFilter,
    doc,
    get_query_args_doc,
)
from atoti_query import QuerySession
from atoti_query._internal import QueryPrivateParameters, generate_mdx, get_cube

from ._docs_utils import EXPLAIN_QUERY_DOC
from ._hierarchy_arguments import HierarchyArguments
from ._java_api import JavaApi
from ._local_hierarchies import LocalHierarchies
from ._local_measures import LocalMeasures
from ._query_plan import QueryAnalysis
from ._runtime_type_checking_utils import typecheck
from .aggregates_cache import AggregatesCache

_LocalMeasures = TypeVar("_LocalMeasures", bound=LocalMeasures[Any])
_LocalHierarchies = TypeVar("_LocalHierarchies", bound=LocalHierarchies[Any])


@typecheck
class LocalCube(BaseCube[_LocalHierarchies, LevelsT, _LocalMeasures]):
    """Local cube class."""

    def __init__(
        self,
        name: str,
        /,
        *,
        aggregates_cache: AggregatesCache,
        create_query_session: Callable[[], QuerySession],
        hierarchies: _LocalHierarchies,
        java_api: JavaApi,
        level_function: Callable[[_LocalHierarchies], LevelsT],
        measures: _LocalMeasures,
        session_name: Optional[str],
    ):
        super().__init__(name, hierarchies=hierarchies, measures=measures)

        self._aggregates_cache = aggregates_cache
        self._create_query_session = create_query_session
        self._java_api = java_api
        self._levels: LevelsT = level_function(self._hierarchies)
        self._session_name = session_name

    @property
    def name(self) -> str:
        """Name of the cube."""
        return self._name

    @property
    def hierarchies(self) -> _LocalHierarchies:
        """Hierarchies of the cube."""
        return self._hierarchies

    @property
    def levels(self) -> LevelsT:
        """Levels of the cube."""
        return self._levels

    @property
    def measures(self) -> _LocalMeasures:
        """Measures of the cube."""
        return self._measures

    @property
    def aggregates_cache(self) -> AggregatesCache:
        """Aggregates cache of the cube."""
        return self._aggregates_cache

    @abstractmethod
    def _get_level_data_types(
        self, levels_coordinates: Iterable[LevelCoordinates], /
    ) -> Dict[LevelCoordinates, DataType]:
        ...

    @doc(QUERY_DOC, args=get_query_args_doc(is_query_session=False))
    def query(
        self,
        *measures: BaseMeasure,
        context: Context = EMPTY_MAPPING,
        filter: Optional[QueryFilter] = None,  # pylint: disable=redefined-builtin
        include_empty_rows: bool = False,
        include_totals: bool = False,
        levels: Iterable[BaseLevel] = (),
        mode: Literal["pretty", "raw"] = "pretty",
        scenario: str = BASE_SCENARIO_NAME,
        timeout: timedelta = timedelta(seconds=30),
        **kwargs: Any,
    ) -> pd.DataFrame:
        query_session = self._create_query_session()

        def get_level_data_types(
            levels_coordinates: Iterable[LevelCoordinates], /, *, cube_name: str
        ) -> Dict[LevelCoordinates, DataType]:
            assert cube_name == self.name
            return self._get_level_data_types(levels_coordinates)

        return query_session.cubes[self.name].query(
            *measures,
            context=context,
            filter=filter,
            get_level_data_types=get_level_data_types,
            include_empty_rows=include_empty_rows,
            include_totals=include_totals,
            levels=levels,
            mode=mode,
            scenario=scenario,
            timeout=timeout,
            **kwargs,
        )

    @doc(EXPLAIN_QUERY_DOC, corresponding_method="query")
    def explain_query(
        self,
        *measures: BaseMeasure,
        filter: Optional[QueryFilter] = None,  # pylint: disable=redefined-builtin
        include_empty_rows: bool = False,
        include_totals: bool = False,
        levels: Iterable[BaseLevel] = (),
        scenario: str = BASE_SCENARIO_NAME,
        timeout: timedelta = timedelta(seconds=30),
        **kwargs: Any,
    ) -> QueryAnalysis:
        query_private_parameters = QueryPrivateParameters(**kwargs)
        filter = query_private_parameters.condition if filter is None else filter

        query_session = self._create_query_session()
        cube = get_cube(self.name, discovery=query_session._discovery)

        mdx = generate_mdx(
            cube=cube,
            filter=filter,
            include_empty_rows=include_empty_rows,
            include_totals=include_totals,
            levels_coordinates=[level._coordinates for level in levels],
            measures_coordinates=[measure._coordinates for measure in measures],
            scenario=scenario,
        )
        return self._java_api.analyze_mdx(mdx, timeout=timeout)

    @abstractmethod
    def _create_hierarchy_from_arguments(
        self, arguments: HierarchyArguments
    ) -> BaseHierarchyBound:
        ...
