from dataclasses import dataclass
from typing import Tuple

from atoti_core import Coordinates


@dataclass(frozen=True)
class ColumnCoordinates(Coordinates):  # pylint: disable=keyword-only-dataclass
    table_name: str
    column_name: str

    @property
    def key(self) -> Tuple[str, str]:
        return self.table_name, self.column_name

    def __repr__(self) -> str:
        return f"""t["{self.table_name}"]["{self.column_name}"]"""
