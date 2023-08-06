from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, Iterable, Mapping, Optional, Protocol

from atoti_core import EMPTY_MAPPING, Constant

from ..type import DataType


class LoadDataIntoTable(Protocol):
    def __call__(
        self,
        *,
        table_name: str,
        source_key: str,
        scenario_name: str,
        source_params: Mapping[str, Any],
    ) -> None:
        ...


class InferTypes(Protocol):
    def __call__(
        self,
        *,
        source_key: str,
        keys: Iterable[str],
        default_values: Mapping[str, Optional[Constant]],
        source_params: Mapping[str, Any],
    ) -> Dict[str, DataType]:
        ...


class DataSource(ABC):
    def __init__(self, *, load_data_into_table: LoadDataIntoTable) -> None:
        super().__init__()

        self._load_data_into_table = load_data_into_table

    @property
    @abstractmethod
    def key(self) -> str:
        ...

    def load_data_into_table(
        self,
        table_name: str,
        *,
        scenario_name: str,
        source_params: Mapping[str, Any] = EMPTY_MAPPING,
    ) -> None:
        """Load the data into an existing table with a given source.

        Args:
            table_name: The name of the table to feed.
            scenario_name: The name of the scenario to feed.
            source_params: The parameters specific to the source.
        """
        self._load_data_into_table(
            table_name=table_name,
            source_key=self.key,
            scenario_name=scenario_name,
            source_params=source_params,
        )
