from typing import Dict, Iterable, Mapping, Optional

from atoti_query import QueryMeasure

from ..._java_api import JavaApi
from ..._local_measures import LocalMeasures


class DistributedMeasures(LocalMeasures[QueryMeasure]):
    def __init__(self, *, cube_name: str, java_api: JavaApi) -> None:
        super().__init__(java_api=java_api)

        self._cube_name = cube_name

    def _get_underlying(self) -> Dict[str, QueryMeasure]:
        """Fetch the measures from the JVM each time they are needed."""
        cube_measures = self._java_api.get_measures(self._cube_name)
        return {
            name: QueryMeasure(
                name,
                description=cube_measures[name].description,
                folder=cube_measures[name].folder,
                formatter=cube_measures[name].formatter,
                visible=cube_measures[name].visible,
            )
            for name in cube_measures
        }

    def __getitem__(self, key: str, /) -> QueryMeasure:
        measure = self._java_api.get_measure(key, cube_name=self._cube_name)
        return QueryMeasure(
            key,
            formatter=measure.formatter,
            folder=measure.folder,
            description=measure.description,
            visible=measure.visible,
        )

    def _update(self, other: Mapping[str, QueryMeasure]) -> None:
        raise AssertionError("Distributed cube measures cannot be changed.")

    def _delete_keys(self, keys: Optional[Iterable[str]] = None, /) -> None:
        raise AssertionError("Distributed cube measures cannot be changed.")
