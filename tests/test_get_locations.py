from pathlib import Path

from nzshm_common.location.location import get_locations, LOCATION_LISTS
from nzshm_common.location.code_location import CodedLocation

LOCATIONS_FILEPATH = Path(__file__).parent / 'fixtures' / 'location_file.csv'


def test_id():
    expected = [
        CodedLocation(lat=-41.3, lon=174.78, resolution=0.001),
        CodedLocation(lat=-36.87, lon=174.77, resolution=0.001),
    ]
    assert get_locations(["WLG", "AKL"]) == expected


def test_list():
    assert len(get_locations(["NZ", "SRWG214"])) == (
        len(LOCATION_LISTS["NZ"]["locations"]) + len(LOCATION_LISTS["SRWG214"]["locations"])
    )


def test_csv():
    expected = [
        CodedLocation(-41.2, 100.2, 0.001),
        CodedLocation(-30.5, 99, 0.001),
    ]
    assert get_locations([LOCATIONS_FILEPATH]) == expected


def test_mix():
    assert len(get_locations(["NZ", LOCATIONS_FILEPATH])) == 2 + len(LOCATION_LISTS["NZ"]["locations"])
