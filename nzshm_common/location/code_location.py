import decimal
from collections import OrderedDict
from dataclasses import dataclass, field
from typing import Iterable, List, Optional

from nzshm_common.constants import DEFAULT_RESOLUTION
from nzshm_common.location.types import LatLon


@dataclass(init=False, unsafe_hash=True)
class CodedLocation:
    """Location resolved to the nearest point on a grid with given resolution (degrees).

    ref https://stackoverflow.com/a/28750072 for  the techniques used here to calculate decimal places.
    """

    lat: float = field(hash=True)
    lon: float = field(hash=True)
    resolution: float = field(hash=True)

    def __init__(self, lat: float, lon: float, resolution: float) -> None:
        """
        Create a CodedLocation instance.

        Arguments:
            lat: latitude
            lon: longitude
            resolution: the resolution used to resolve the location
        """
        assert 0 < resolution < 180, "Resolution must be between 0 and 180 degrees."

        self.grid_res = decimal.Decimal(str(resolution).rstrip("0"))
        self.display_places = max(abs(self.grid_res.as_tuple().exponent), 1)  # type: ignore

        div_res = 1 / float(self.grid_res)
        places = abs(decimal.Decimal(div_res).as_tuple().exponent)  # type: ignore

        self.lon = round(lon * div_res, places) / div_res
        self.lat = round(lat * div_res, places) / div_res
        self.resolution = resolution

        self._code = f"{self.lat:.{self.display_places}f}~{self.lon:.{self.display_places}f}"

    def __lt__(self, other: "CodedLocation"):
        """
        Less-than comparator to enable sorting for CodedLocations.

        For arithmetic comparisons we expect:

        * north comes before south
        * when on the same latitude, west comes before east

        Note:
            Coded locations at different resolutions are not considered
            equal. Use `.as_tuple` to check for numerical equivalency.

        Examples:
            >>> origin = CodedLocation(-11.11, 111.11, resolution=0.001)
            >>> origin == CodedLocation(-11.11, 111.11, resolution=0.001)  # Equal
            True
            >>> origin == CodedLocation(-11.11, 111.11, resolution=0.01)  # Wrong resolution
            False

            >>> origin < CodedLocation(-11.12, 111.11, resolution=0.001)  # South of origin
            False
            >>> origin < CodedLocation(-11.10, 111.11, resolution=0.001)  # North of origin
            True
            >>> origin < CodedLocation(-11.11, 111.10, resolution=0.001)  # West of origin
            False
            >>> origin < CodedLocation(-11.11, 111.12, resolution=0.001)  # East of origin
            True

        """
        lat_delta = self.lat - other.lat
        lon_delta = self.lon - other.lon
        if lat_delta > 0:
            return True
        elif lat_delta < 0:
            return False
        elif lon_delta < 0:
            return True
        else:
            return False

    @property
    def as_tuple(self) -> LatLon:
        """
        Convert to a `LatLon(latitude, longitude)` named tuple.

        Example:
            ```py
            >>> from nzshm_common import location
            >>> location.get_locations(["CHC"])[0]
            CodedLocation(lat=-43.53, lon=172.63, resolution=0.001)
            >>> latitude, longitude = location.get_locations(["CHC"])[0].as_tuple
            >>> latitude
            -43.53
            ```
        """
        return LatLon(self.lat, self.lon)

    @property
    def code(self) -> str:
        """
        The string code for the location expressed as latitude~longitude.
        """
        return self._code

    @classmethod
    def from_tuple(cls, location: LatLon, resolution: float = DEFAULT_RESOLUTION) -> "CodedLocation":
        """
        Create a `CodedLocation` from a tuple.

        Parameters:
            location: a structure containing a latitude and longitude, in that order
            resolution: coordinate resolution in degrees

        Examples:
            Convert a single location:
            >>> from nzshm_common import CodedLocation
            >>> CodedLocation.from_tuple((-36.87, 174.77))
            CodedLocation(lat=-36.87, lon=174.77, resolution=0.001)

            >>> from nzshm_common import LatLon
            >>> CodedLocation.from_tuple(LatLon(-36.87, 174.77))
            CodedLocation(lat=-36.87, lon=174.77, resolution=0.001)

            Convert a list of locations:
            >>> location_list = [(-36.111, 174.111), (-36.222, 174.222)]
            >>> list(map(CodedLocation.from_tuple, location_list))
            [
                CodedLocation(lat=-36.111, lon=174.111, resolution=0.001),
                CodedLocation(lat=-36.222, lon=174.222, resolution=0.001)
            ]

            Convert a list of locations with a custom resolution:
            >>> from functools import partial
            >>> lo_res = partial(CodedLocation.from_tuple, resolution=0.1)
            >>> list(map(lo_res, location_list))
            [
                CodedLocation(lat=-36.1, lon=174.1, resolution=0.1),
                CodedLocation(lat=-36.2, lon=174.2, resolution=0.1)
            ]
        """
        return CodedLocation(lat=location[0], lon=location[1], resolution=resolution)

    def resample(self, resolution: float) -> "CodedLocation":
        """
        Create a resampled CodedLocation with a finer resolution.
        """
        return self.downsample(resolution)

    def downsample(self, resolution: float) -> "CodedLocation":
        """
        Create a downsampled CodedLocation with a coarser resolution.
        """
        return CodedLocation(lat=self.lat, lon=self.lon, resolution=resolution)


class CodedLocationBin:
    """
    A collection of CodedLocation values, gathered into bins at a coarser resolution.
    """

    reference_point: CodedLocation
    locations: List[CodedLocation]
    bin_resolution: float
    _code: str

    def __init__(
        self, reference_point: CodedLocation, bin_resolution: float, locations: Optional[Iterable[CodedLocation]] = None
    ):
        """
        Create a CodedLocationBin instance.

        Arguments:
            reference_point: the downsampled coordinate use as a reference point for the collection.
            bin_resolution: the coarser-level resolution of the bin
            locations: a collection of CodedLocation values
        """
        self.reference_point = reference_point
        self.bin_resolution = bin_resolution

        if locations is not None:
            self.locations: List[CodedLocation] = list(locations)
        else:
            self.locations: List[CodedLocation] = list()

    def __iter__(self):
        """Iterate over the location collection."""
        return self.locations.__iter__()

    def __len__(self):
        """Count the number of locations in the bin."""
        return len(self.locations)

    def __repr__(self):
        plural = "" if len(self.locations) == 1 else "s"
        count = len(self)
        code = self.reference_point.code
        resolution = self.bin_resolution

        return f"CodedLocationBin({count} location{plural} near {code} below resolution {resolution})"

    @property
    def code(self) -> str:
        """
        The string code for the reference point, expressed as latitude~longitude.

        This can be used as a unique key when collecting a dictionary of bins.
        """
        return self.reference_point.code


def bin_locations(
    locations: Iterable[CodedLocation], at_resolution: float, sort_bins: bool = True
) -> OrderedDict[str, CodedLocationBin]:
    """
    Collect CodedLocations into a dictionary of bins with coarser resolution.

    Bin selection is based on the `CodedLocation.downsample` method, reducing
    coordinate precision.

    Bins are keyed on the `CodedLocation.code` property.

    TODO: emit a warning if at_resolution is lower than incoming resolutions?

    Examples:
        >>> from nzshm_common import grids, location
        >>> grid_locs = grids.get_location_grid('NZ_0_1_NB_1_1', resolution=0.1)
        >>> grid_bins = bin_locations(grid_locs, at_resolution=0.5)
        >>> for location_bin in grid_bins:
        ...     for coded_loc in bin:
        ...         # Do a thing
    """
    bin_dict: OrderedDict[str, CodedLocationBin] = OrderedDict()

    for location in locations:
        coded_loc = location.downsample(at_resolution)
        bin_code = coded_loc._code
        if bin_code not in bin_dict:
            bin_dict[bin_code] = CodedLocationBin(coded_loc, at_resolution, [])

        bin_dict[bin_code].locations.append(location)

    if sort_bins:
        # Sort the bins themselves.
        bin_dict = OrderedDict(sorted(bin_dict.items(), key=lambda item: item[1].reference_point))

        # Sort CodedLocations within each bin.
        for location_bin in bin_dict.values():
            location_bin.locations.sort()

    return bin_dict
