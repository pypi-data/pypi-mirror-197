from __future__ import annotations

from typing import Mapping

from atoti_core import BaseHierarchy
from typeguard import typeguard_ignore

from ._java_api import JavaApi
from ._level_arguments import LevelArguments
from .level import Level


@typeguard_ignore
class Hierarchy(BaseHierarchy[Level]):
    """Hierarchy of a :class:`atoti.Cube`.

    A hierarchy is a sub category of a :attr:`~dimension` and represents a precise type of data.

    For example, :guilabel:`Quarter` or :guilabel:`Week` could be hierarchies in the :guilabel:`Time` dimension.
    """

    def __init__(
        self,
        name: str,
        /,
        *,
        cube_name: str,
        dimension: str,
        java_api: JavaApi,
        levels_arguments: Mapping[str, LevelArguments],
        slicing: bool,
        visible: bool,
        virtual: bool,
    ) -> None:
        super().__init__(name, dimension=dimension)

        self._cube_name = cube_name
        self._java_api = java_api
        self._slicing = slicing
        self._visible = visible
        self._virtual = virtual

        self._levels: Mapping[str, Level] = {
            level_name: Level(
                level_arguments[0],
                column_name=level_arguments[1].column_name,
                cube_name=self._cube_name,
                data_type=level_arguments[2],
                hierarchy_coordinates=self._coordinates,
                java_api=self._java_api,
                order=level_arguments[3],
                table_name=level_arguments[1].table_name,
            )
            for level_name, level_arguments in levels_arguments.items()
        }

    @property
    def name(self) -> str:
        return self._name

    @property
    def levels(self) -> Mapping[str, Level]:
        return self._levels

    @property
    def virtual(self) -> bool:
        """
        Whether the hierarchy is virtual or not.

        A virtual hierarchy is a lightweight hierarchy which does not store in memory the list of its members.
        It is useful for hierarchies with large cardinality.
        """
        return self._virtual

    @virtual.setter
    def virtual(self, virtual: bool, /) -> None:
        self._java_api.update_hierarchy_virtual(
            cube_name=self._cube_name,
            hierarchy_coordinates=self._coordinates,
            virtual=virtual,
        )
        self._java_api.refresh()
        self._virtual = virtual

    @property
    def dimension(self) -> str:
        """Name of the dimension of the hierarchy.

        Note:
            If all the hierarchies in a dimension have their deepest level of type ``TIME``, the dimension's type will be set to ``TIME`` too.
            This can be useful for some clients such as Excel which rely on the dimension's type to be ``TIME`` to decide whether to display date filters.

        """
        return self._dimension

    @dimension.setter
    def dimension(self, value: str) -> None:
        self._java_api.update_hierarchy_coordinate(
            cube_name=self._cube_name,
            hierarchy_coordinates=self._coordinates,
            new_dim=value,
            new_hierarchy=self._name,
        )
        self._java_api.refresh()
        self._dimension = value

    @property
    def slicing(self) -> bool:
        return self._slicing

    @slicing.setter
    def slicing(self, value: bool) -> None:
        """Slicing setter."""
        self._java_api.update_hierarchy_slicing(
            cube_name=self._cube_name,
            hierarchy_coordinates=self._coordinates,
            slicing=value,
        )
        self._java_api.refresh()
        self._slicing = value

    @property
    def visible(self) -> bool:
        """Whether the hierarchy is visible or not."""
        return self._visible

    @visible.setter
    def visible(self, value: bool) -> None:
        """Visibility setter."""
        self._java_api.set_hierarchy_visibility(
            cube_name=self._cube_name,
            dimension=self._dimension,
            name=self._name,
            visible=value,
        )
        self._java_api.refresh()
        self._visible = value
