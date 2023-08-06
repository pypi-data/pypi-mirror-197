from typeguard import typeguard_ignore

from ._local_cubes import LocalCubes
from .cube import Cube


@typeguard_ignore
class Cubes(LocalCubes[Cube]):
    """Manage the cubes of the session."""
