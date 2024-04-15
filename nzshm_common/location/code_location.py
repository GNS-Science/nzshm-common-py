import decimal
from dataclasses import dataclass, field
from typing import Tuple, Union

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

    @property
    def as_tuple(self) -> LatLon:
        """
        Convert to a `LatLon(latitude, longitude)` named tuple.

        Example:
            ```py
            >>> nzshm_common.location.get_locations(["CHC"])[0]
            CodedLocation(lat=-43.53, lon=172.63, resolution=0.001)
            >>> nzshm_common.location.get_locations(["CHC"])[0].as_tuple.latitude
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
    def from_tuple(
        cls, location: Union[LatLon, Tuple[float, float]], resolution: float = DEFAULT_RESOLUTION
    ) -> "CodedLocation":
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
        """Downsample/Resample."""
        return self.downsample(resolution)

    def downsample(self, resolution: float) -> "CodedLocation":
        """Downsample/Resample."""
        return CodedLocation(lat=self.lat, lon=self.lon, resolution=resolution)
