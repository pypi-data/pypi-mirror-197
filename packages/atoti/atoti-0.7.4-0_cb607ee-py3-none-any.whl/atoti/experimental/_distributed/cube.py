from __future__ import annotations

from typing import Callable, Dict, Iterable, Optional

from atoti_core import DataType, LevelCoordinates
from atoti_query import QueryHierarchy, QueryLevel, QuerySession
from typeguard import typeguard_ignore

from ..._hierarchy_arguments import HierarchyArguments
from ..._java_api import JavaApi
from ..._local_cube import LocalCube
from ...aggregates_cache import AggregatesCache
from .hierarchies import DistributedHierarchies
from .levels import DistributedLevels
from .measures import DistributedMeasures


class DistributedCube(
    LocalCube[DistributedHierarchies, DistributedLevels, DistributedMeasures]
):
    """Cube of a distributed session."""

    @typeguard_ignore
    def __init__(
        self,
        name: str,
        /,
        *,
        create_query_session: Callable[[], QuerySession],
        java_api: JavaApi,
        session_name: Optional[str],
    ):
        super().__init__(
            name,
            aggregates_cache=AggregatesCache(
                cube_name=name,
                get_capacity=java_api.get_aggregates_cache_capacity,
                set_capacity=java_api.set_aggregates_cache_capacity,
            ),
            create_query_session=create_query_session,
            hierarchies=DistributedHierarchies(
                create_hierarchy_from_arguments=self._create_hierarchy_from_arguments,
                cube_name=name,
                java_api=java_api,
            ),
            java_api=java_api,
            level_function=lambda hierarchies: DistributedLevels(
                hierarchies=hierarchies
            ),
            measures=DistributedMeasures(cube_name=name, java_api=java_api),
            session_name=session_name,
        )

    def _get_level_data_types(
        self, levels_coordinates: Iterable[LevelCoordinates], /
    ) -> Dict[LevelCoordinates, DataType]:
        return {level_coordinates: "Object" for level_coordinates in levels_coordinates}

    def _create_hierarchy_from_arguments(
        self, arguments: HierarchyArguments
    ) -> QueryHierarchy:
        hierarchy = QueryHierarchy(
            arguments.name,
            dimension=arguments.dimension,
            levels={
                level_name: QueryLevel(
                    level_name,
                    dimension=arguments.dimension,
                    hierarchy=arguments.name,
                )
                for level_name in arguments.levels_arguments
                if level_name != "ALL"
            },
            slicing=arguments.slicing,
        )
        return hierarchy
