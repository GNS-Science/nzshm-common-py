from collections import namedtuple
from enum import Enum
from functools import partial
from typing import Iterable, Tuple

from nzshm_common.constants import DEFAULT_RESOLUTION
from nzshm_common.grids.nz_0_1_nb_1_v0 import NZ01nb1v0
from nzshm_common.grids.nz_0_1_nb_1_v1 import NZ01nb1v1
from nzshm_common.grids.nz_0_2_nb_1_1 import NZ_0_2_nb_1_1
from nzshm_common.grids.wlg_0_01_nb_1_1 import WLG_0_01_nb_1_1
from nzshm_common.grids.wlg_0_05_nb_1_1 import WLG_0_05_nb_1_1
from nzshm_common.location.code_location import CodedLocation

RegionGridEntry = namedtuple("RegionGridEntry", "region_name resolution neighbours grid version")


class RegionGrid(Enum):
    NZ_0_1_NB_1_0 = RegionGridEntry(region_name="NZ", resolution=0.1, neighbours=1, grid=NZ01nb1v0(), version=0)
    NZ_0_1_NB_1_1 = RegionGridEntry(region_name="NZ", resolution=0.1, neighbours=1, grid=NZ01nb1v1(), version=1)
    NZ_0_2_NB_1_1 = RegionGridEntry(region_name="NZ", resolution=0.2, neighbours=1, grid=NZ_0_2_nb_1_1(), version=1)

    WLG_0_01_nb_1_1 = RegionGridEntry(
        region_name="WLG",
        resolution=0.01,
        neighbours=1,
        grid=WLG_0_01_nb_1_1(),
        version=1,
    )
    WLG_0_05_nb_1_1 = RegionGridEntry(
        region_name="WLG",
        resolution=0.05,
        neighbours=1,
        grid=WLG_0_05_nb_1_1(),
        version=1,
    )

    def __init__(self, region_name, resolution, neighbours, grid, version):
        self.region_name = region_name
        self.resolution = resolution
        self.neighbours = neighbours
        self.grid = grid

    def load(self):
        return self.grid.load()


def load_grid(gri_name: str) -> list[Tuple[float, float]]:
    return RegionGrid[gri_name].load()


def get_grid_locations(location_grid_name: str, resolution=DEFAULT_RESOLUTION) -> Iterable[CodedLocation]:
    grid_values = RegionGrid[location_grid_name].load()
    coded_at_resolution = partial(CodedLocation.from_tuple, resolution=resolution)
    return list(map(coded_at_resolution, grid_values))
