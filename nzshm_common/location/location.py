# Omitting country for now, focus on NZ
# https://service.unece.org/trade/locode/nz.htm
LOCATIONS = [
    {"id": "AKL", "name": "Auckland", "latitude": -36.87, "logitude": 174.77, "backarc": True},
    {"id": "BHE", "name": "Blenheim", "latitude": -41.51, "logitude": 173.95, "backarc": False},
    {"id": "CHC", "name": "Christchurch", "latitude": -43.53, "logitude": 172.63, "backarc": False},
    {"id": "DUD", "name": "Dunedin", "latitude": -45.87, "logitude": 170.5, "backarc": False},
    {"id": "GIS", "name": "Gisborne", "latitude": -38.65, "logitude": 178.0, "backarc": False},
    {"id": "GMN", "name": "Greymouth", "latitude": -42.45, "logitude": 171.21, "backarc": False},
    {"id": "HAW", "name": "Hawera", "latitude": -39.59, "logitude": 174.28, "backarc": True},
    {"id": "HLZ", "name": "Hamilton", "latitude": -37.78, "logitude": 175.28, "backarc": True},
    {"id": "IVC", "name": "Invercargill", "latitude": -46.43, "logitude": 168.36, "backarc": False},
    {"id": "KBZ", "name": "Kaikoura", "latitude": -42.4, "logitude": 173.68, "backarc": False},
    {"id": "KKE", "name": "Kerikeri", "latitude": -35.22, "logitude": 173.97, "backarc": True},
    {"id": "LVN", "name": "Levin", "latitude": -40.63, "logitude": 175.28, "backarc": False},
    {"id": "MON", "name": "Mount Cook", "latitude": -43.73, "logitude": 170.1, "backarc": False},
    {"id": "MRO", "name": "Masterton", "latitude": -40.96, "logitude": 175.66, "backarc": False},
    {"id": "NPE", "name": "Napier", "latitude": -39.48, "logitude": 176.92, "backarc": False},
    {"id": "NPL", "name": "New Plymouth", "latitude": -39.07, "logitude": 174.08, "backarc": True},
    {"id": "NSN", "name": "Nelson", "latitude": -41.27, "logitude": 173.28, "backarc": False},
    {"id": "PMR", "name": "Palmerston North", "latitude": -40.35, "logitude": 175.62, "backarc": False},
    {"id": "TEU", "name": "Te Anau", "latitude": -45.41, "logitude": 167.72, "backarc": False},
    {"id": "TIU", "name": "Timaru", "latitude": -44.4, "logitude": 171.26, "backarc": False},
    {"id": "TKZ", "name": "Tokoroa", "latitude": -38.23, "logitude": 175.87, "backarc": True},
    {"id": "TMZ", "name": "Thames", "latitude": -37.13, "logitude": 175.53, "backarc": True},
    {"id": "TRG", "name": "Tauranga", "latitude": -37.69, "logitude": 176.17, "backarc": True},
    {"id": "TUO", "name": "Taupo", "latitude": -38.68, "logitude": 176.08, "backarc": True},
    {"id": "ROT", "name": "Rotorua", "latitude": -38.14, "logitude": 176.25, "backarc": True},
    {"id": "WHK", "name": "Whakatane", "latitude": -37.98, "logitude": 177.0, "backarc": False},
    {"id": "WHO", "name": "Franz Josef", "latitude": -43.35, "logitude": 170.17, "backarc": False},
    {"id": "WLG", "name": "Wellington", "latitude": -41.3, "logitude": 174.78, "backarc": False},
    {"id": "WSZ", "name": "Westport", "latitude": -41.75, "logitude": 171.58, "backarc": False},
    {"id": "xx1", "name": "Whanganui", "latitude": -39.93, "logitude": 175.05, "backarc": False},
    {"id": "xx2", "name": "Turangi", "latitude": -39.0, "logitude": 175.93, "backarc": False},
    {"id": "xx3", "name": "Otira", "latitude": -42.78, "logitude": 171.54, "backarc": False},
    {"id": "xx4", "name": "Haast", "latitude": -43.88, "logitude": 169.06, "backarc": False},
    {"id": "xx5", "name": "Hanmer Springs", "latitude": -42.54, "logitude": 172.78, "backarc": False},
    {"id": "ZQN", "name": "Queenstown", "latitude": -45.02, "logitude": 168.69, "backarc": False},
]

LOCATIONS_BY_ID = {location["id"]: location for location in LOCATIONS}

LOCATION_LISTS = [
    {
        "id": "NZ",
        "name": "Default NZ locations",
        "locations": list(map(lambda loc: loc["id"], LOCATIONS)),
    },
    {
        "id": "NZ2",
        "name": "Main Cities NZ",
        "locations": ["WLG", "CHC", "DUD", "NPL", "AKL", "ROT", "HLZ"],
    },
]


def location_by_id(location_code):
    return LOCATIONS_BY_ID[location_code]


if __name__ == "__main__":
    """Print all locations."""
    print("custom_site_id,lon,lat")
    for loc in LOCATIONS:
        print(f"{loc['id']},{loc['longitude']},{loc['latitude']}")
