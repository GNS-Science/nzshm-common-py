import decimal
from dataclasses import dataclass, field

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

    def resample(self, resolution: float) -> "CodedLocation":
        """Downsample/Resample."""
        return self.downsample(resolution)

    def downsample(self, resolution: float) -> "CodedLocation":
        """Downsample/Resample."""
        return CodedLocation(lat=self.lat, lon=self.lon, resolution=resolution)
