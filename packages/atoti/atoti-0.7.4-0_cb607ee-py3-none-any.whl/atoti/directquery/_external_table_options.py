from abc import ABC
from typing import Generic, Mapping, Optional, Sequence, Union

from atoti_core import EMPTY_MAPPING

from ..directquery import MultiColumnArrayConversion, MultiRowArrayConversion
from ._external_table import ExternalTableT


class ExternalTableOptions(Generic[ExternalTableT], ABC):
    def __init__(
        self,
        *,
        array_conversion: Optional[
            Union[MultiColumnArrayConversion, MultiRowArrayConversion]
        ] = None,
        keys: Optional[Sequence[str]] = None,
        options: Mapping[str, object] = EMPTY_MAPPING,
    ) -> None:
        super().__init__()

        self._array_conversion = array_conversion
        self._keys = keys
        self._options = options
