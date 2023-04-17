import argparse
import csv

from enum import Enum
from pathlib import Path

from shapely.geometry import Point

from nzshm_common.location.location import LOCATIONS_BY_ID, LOCATIONS_SRWG214_BY_ID
from nzshm_common.geometry.geometry import create_backarc_polygon


class SiteLists(Enum):
    NZ36 = "NZ36"
    SRWG214 = "SRWG214"
    BOTH = "NZ36 and SRWG214"


def site_list(loc_by_id):
    sites = []
    for location in loc_by_id.values():
        point = Point(location['longitude'], location['latitude'])
        ba_flag = int(create_backarc_polygon().contains(point))
        sites.append((location['id'], location['longitude'], location['latitude'], ba_flag))
    return sites


def get_sites(location_list):

    sites = []
    if (location_list is SiteLists.NZ36) | (location_list is SiteLists.BOTH):
        sites += site_list(LOCATIONS_BY_ID)
    if (location_list is SiteLists.SRWG214) | (location_list is SiteLists.BOTH):
        sites += site_list(LOCATIONS_SRWG214_BY_ID)

    return sites


def write_sites(output_path, sites):
    with open(output_path, 'w') as out_file:
        writer = csv.writer(out_file)
        writer.writerow(("custom_site_id", "lon", "lat", "backarc"))
        for site in sites:
            writer.writerow(site)


def main():
    list_choices = [el.name for el in SiteLists]
    parser = argparse.ArgumentParser(
        description="convert locations to OpenQuake site model csv file including backarc flag"
    )
    parser.add_argument(
        "--location-list", "-l", choices=list_choices, default="NZ36", type=str.upper, help="which location list to use"
    )
    parser.add_argument("output_path", help="path of output file")
    args = parser.parse_args()

    output_path = Path(args.output_path)
    if output_path.exists():
        raise Exception("output file %s already exists" % output_path)

    print(f"creating OpenQuake site file for {SiteLists[args.location_list].value}")
    location_list = SiteLists[args.location_list]
    sites = get_sites(location_list)
    write_sites(output_path, sites)


if __name__ == "__main__":
    main()
