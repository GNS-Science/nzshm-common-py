import decimal
from dataclasses import dataclass


@dataclass
class CodedLocation:

    lat: float
    lon: float
    code: str = ""

    # def set_code(self, code):
    #     self.code = code

    def downsample(self, resolution: float) -> "CodedLocation":
        """Downsamples to the nearest point on a grid with given resolution (degrees).

        # ref https://stackoverflow.com/a/28750072 for  the techniques used here to calculate decimal places.
        """
        assert 0 < resolution < 180
        grid_res = decimal.Decimal(str(resolution).rstrip("0"))
        display_places = max(abs(grid_res.as_tuple().exponent), 1)

        div_res = 1 / float(grid_res)
        places = abs(decimal.Decimal(div_res).as_tuple().exponent)

        # print(f'grid_res {grid_res} => div_res {div_res} places {places}') #  round_res {round_res}

        d_lon = round(self.lon * div_res, places) / div_res
        d_lat = round(self.lat * div_res, places) / div_res

        return CodedLocation(
            code=f"{d_lat:.{display_places}f}~{d_lon:.{display_places}f}",
            lat=d_lat,
            lon=d_lon,
        )
