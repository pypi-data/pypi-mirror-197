from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Dict,
    Iterable,
    Mapping,
    Optional,
    Tuple,
    Union,
    overload,
)

from typeguard import typeguard_ignore

from ._java_api import JavaApi
from ._local_measures import LocalMeasures
from ._measure_convertible import MeasureConvertible
from ._measure_definition import MeasureDefinition, get_measure_convertible_and_metadata
from ._measure_description import MeasureDescription, convert_to_measure_description
from ._measure_metadata import MeasureMetadata
from .measure import Measure

if TYPE_CHECKING:
    from _typeshed import SupportsKeysAndGetItem  # pylint: disable=nested-import


def _validate_name(name: str, /) -> None:
    if "," in name:
        raise ValueError(f'Invalid measure name "{name}". "," are not allowed.')
    if name != name.strip():
        raise ValueError(
            f'Invalid measure name "{name}". Leading or trailing whitespaces are not allowed.'
        )
    if name.startswith("__hidden_"):
        raise ValueError(
            f'Invalid measure name "{name}". Name cannot start with "__hidden_".'
        )


class Measures(LocalMeasures[Measure]):
    """Manage the measures."""

    def __init__(
        self,
        *,
        cube_name: str,
        java_api: JavaApi,
    ):
        super().__init__(java_api=java_api)

        self._cube_name = cube_name

    @typeguard_ignore
    def _build_measure(
        self, name: str, description: JavaApi.JavaMeasureDescription
    ) -> Measure:
        return Measure(
            name,
            cube_name=self._cube_name,
            data_type=description.underlying_type,
            description=description.description,
            folder=description.folder,
            formatter=description.formatter,
            java_api=self._java_api,
            visible=description.visible,
        )

    def _get_underlying(self) -> Dict[str, Measure]:
        """Fetch the measures from the JVM each time they are needed."""
        cube_measures = self._java_api.get_measures(self._cube_name)
        return {
            name: self._build_measure(name, cube_measures[name])
            for name in cube_measures
        }

    def __getitem__(self, key: str, /) -> Measure:
        cube_measure = self._java_api.get_measure(key, cube_name=self._cube_name)
        return self._build_measure(key, cube_measure)

    # Custom override with same value type as the one used in `update()`.
    def __setitem__(self, key: str, value: MeasureConvertible, /) -> None:
        self.update({key: value})

    @overload
    def update(
        self,
        __m: SupportsKeysAndGetItem[str, MeasureDefinition],
        **kwargs: MeasureDefinition,
    ) -> None:
        ...

    @overload
    def update(
        self,
        __m: Iterable[Tuple[str, MeasureDefinition]],
        **kwargs: MeasureDefinition,
    ) -> None:
        ...

    @overload
    def update(self, **kwargs: MeasureDefinition) -> None:
        ...

    # Custom override types on purpose so that measure convertible objects can be inserted.
    def update(  # type: ignore
        # pylint: disable=too-many-branches
        self,
        __m: Optional[
            Union[
                Mapping[str, MeasureDefinition],
                Iterable[Tuple[str, MeasureDefinition]],
            ]
        ] = None,
        **kwargs: MeasureDefinition,
    ) -> None:
        other: Dict[str, MeasureDefinition] = {}

        if __m is not None:
            other.update(__m)
        other.update(**kwargs)

        self._update(
            {
                measure_name: get_measure_convertible_and_metadata(measure_definition)
                for measure_name, measure_definition in other.items()
            }
        )

    # Custom override types on purpose so that measure-like objects can be inserted.
    def _update(  # type: ignore
        self,
        other: Mapping[str, Tuple[MeasureConvertible, MeasureMetadata]],
    ) -> None:
        for measure_name, (
            measure,
            measure_metadata,
        ) in other.items():
            _validate_name(measure_name)

            if not isinstance(measure, MeasureDescription):
                measure = convert_to_measure_description(measure)

            try:
                measure._distil(
                    java_api=self._java_api,
                    cube_name=self._cube_name,
                    measure_name=measure_name,
                    measure_metadata=measure_metadata,
                )
            except AttributeError as err:
                raise ValueError(f"Cannot create a measure from {measure}") from err

        self._java_api.publish_measures(self._cube_name)

    def _delete_keys(self, keys: Optional[Iterable[str]] = None, /) -> None:
        keys = self._default_to_all_keys(keys)
        for key in keys:
            self._java_api.delete_measure(key, cube_name=self._cube_name)
