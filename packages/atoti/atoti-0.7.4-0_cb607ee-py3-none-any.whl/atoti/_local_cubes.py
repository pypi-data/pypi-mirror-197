from typing import Any, Dict, Iterable, Mapping, Optional, Protocol, TypeVar, cast

from atoti_core import BaseCubes

from ._delegate_mutable_mapping import DelegateMutableMapping
from ._local_cube import LocalCube

_LocalCube = TypeVar("_LocalCube", bound="LocalCube[Any, Any, Any]", covariant=True)


class _DeleteCube(Protocol):
    def __call__(self, cube_name: str, /) -> None:
        ...


class _GetCube(Protocol[_LocalCube]):
    def __call__(self, cube_name: str, /) -> _LocalCube:
        ...


class _GetCubes(Protocol[_LocalCube]):
    def __call__(self) -> Mapping[str, _LocalCube]:
        ...


class LocalCubes(
    DelegateMutableMapping[
        str,
        _LocalCube,  # pyright: ignore[reportGeneralTypeIssues]
    ],
    BaseCubes[_LocalCube],
):
    def __init__(
        self,
        *,
        delete_cube: _DeleteCube,
        get_cube: _GetCube[_LocalCube],
        get_cubes: _GetCubes[_LocalCube],
    ) -> None:
        super().__init__()

        self._delete_cube = delete_cube
        self._get_cube = get_cube
        self._get_cubes = get_cubes

    def _update(self, other: Mapping[str, _LocalCube], /) -> None:
        raise AssertionError("Use `Session.create_cube()` to create a cube.")

    def __getitem__(self, key: str, /) -> _LocalCube:
        return self._get_cube(key)

    def _get_underlying(self) -> Dict[str, _LocalCube]:
        return cast(Dict[str, _LocalCube], self._get_cubes())

    def _delete_keys(self, keys: Optional[Iterable[str]] = None, /) -> None:
        keys = self._default_to_all_keys(keys)
        for key in keys:
            self._delete_cube(key)
