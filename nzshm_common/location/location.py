import json
from pathlib import Path

# Omitting country for now, focus on NZ
# https://service.unece.org/trade/locode/nz.htm

locations_filepath = Path(Path(__file__).parent, 'locations.json')
with open(locations_filepath, 'r') as locations_file:
    LOCATIONS = json.load(locations_file)

LOCATIONS_BY_ID = {location["id"]: location for location in LOCATIONS}


LOCATION_LISTS = {

    "NZ":{
        "id": "NZ",
        "name": "Default NZ locations",
        "locations": [loc["id"] for loc in LOCATIONS if "srg" not in loc["id"]]
    },

    "NZ2":{
        "id": "NZ2",
        "name": "Main Cities NZ",
        "locations": ["WLG", "CHC", "DUD", "NPL", "AKL", "ROT", "HLZ"],
    },

    "SRWG214":{
        "id": "SRWG214",
        "name": "Seismic Risk Working Group NZ code locations",
        "locations": list(map(lambda idn: f"srg_{idn}", range(214))),
    },
    
    "ALL":{
        "id": "ALL",
        "name": "Seismic Risk Working Group NZ code locations",
        "locations": list(map(lambda loc: loc["id"], LOCATIONS)),
    },
}


def location_by_id(location_code):
    return LOCATIONS_BY_ID.get(location_code)


if __name__ == "__main__":
    """Print all locations."""
    print("custom_site_id,lon,lat")
    for loc in LOCATIONS:
        print(f"{loc['id']},{loc['longitude']},{loc['latitude']}")
