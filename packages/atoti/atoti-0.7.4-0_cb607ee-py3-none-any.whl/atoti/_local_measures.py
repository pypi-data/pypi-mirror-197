from abc import abstractmethod
from typing import Dict, TypeVar

from atoti_core import BaseMeasures
from atoti_query import QueryMeasure
from typeguard import typechecked, typeguard_ignore

from ._delegate_mutable_mapping import DelegateMutableMapping
from ._java_api import JavaApi
from .measure import Measure

_Measure = TypeVar("_Measure", Measure, QueryMeasure)


@typeguard_ignore
class LocalMeasures(DelegateMutableMapping[str, _Measure], BaseMeasures[_Measure]):
    """Local measures class."""

    def __init__(self, *, java_api: JavaApi) -> None:
        super().__init__()

        self._java_api = java_api

    @abstractmethod
    def _get_underlying(self) -> Dict[str, _Measure]:
        """Fetch the measures from the JVM each time they are needed."""

    @typechecked
    @abstractmethod
    def __getitem__(self, key: str, /) -> _Measure:
        """Return the measure with the given name."""
