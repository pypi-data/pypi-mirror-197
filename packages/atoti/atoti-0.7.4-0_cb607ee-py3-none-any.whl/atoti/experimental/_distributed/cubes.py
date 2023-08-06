from typeguard import typeguard_ignore

from ..._local_cubes import LocalCubes
from .cube import DistributedCube


@typeguard_ignore
class DistributedCubes(LocalCubes[DistributedCube]):
    """Manage the distributed cubes."""
