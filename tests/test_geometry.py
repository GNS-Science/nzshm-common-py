import unittest
import math
import random
import geopandas as gpd

from nzshm_common.geometry.geometry import create_hexagon, create_square_tile
from nzshm_common.grids import load_grid


def create_hexgrid(bbox, side):
    """
    returns an array of Points describing hexagons centers that are inside the given bounding_box
    :param bbox: The containing bounding box. The bbox coordinate should be in Webmercator.
    :param side: The size of the hexagons'
    :return: The hexagon grid
    """
    pass


class TestHex(unittest.TestCase):
    def test_create_hexagon(self):

        RESOLUTION = 1  # degrees / km ???
        edge = math.sqrt(RESOLUTION**2 / (3 / 2 * math.sqrt(3)))

        hex = create_hexagon(edge, x=-45, y=175)
        print(hex)
        self.assertAlmostEqual(-45, hex.centroid.bounds[0])  # latitude
        self.assertAlmostEqual(175, hex.centroid.bounds[1])  # longiutude

    def test_adjacent_hexagons_pt2(self):
        """Get some 0.2 degree locations, check we can buld adjacent hexagons."""

        RESOLUTION = 0.2  # degrees / km ???
        edge = math.sqrt(RESOLUTION**2 / (3 / 2 * math.sqrt(3)))

        print(f'edge length {edge}')
        grid = load_grid('NZ_0_2_NB_1_1')

        cells = []
        for pt in grid[30:33]:
            cells.append(create_hexagon(edge, *pt))

        for cell in cells:
            print(cell.centroid, cell.bounds[2] - cell.bounds[0])

        print('centroid spacing', cells[0].centroid.distance(cells[1].centroid))
        print('cell center to boundary', cells[0].centroid.distance(cells[0].boundary))
        print('cell spacing', cells[0].distance(cells[1]))

        self.assertEqual(cells[0].distance(cells[1]), 0.0)

    def test_adjacent_hexagons_pt1(self):
        """Get some 0.1 degree locations, check we can buld adjacent hexagons."""

        RESOLUTION = 0.1  # degrees / km ???
        edge = math.sqrt(RESOLUTION**2 / (3 / 2 * math.sqrt(3)))

        print(f'edge length {edge}')
        grid = load_grid('NZ_0_1_NB_1_1')

        cells = []
        for pt in grid[30:33]:
            cells.append(create_hexagon(edge, *pt))

        for cell in cells:
            print(cell.centroid, cell.bounds[2] - cell.bounds[0])

        print('centroid spacing', cells[0].centroid.distance(cells[1].centroid))
        print('cell center to boundary', cells[0].centroid.distance(cells[0].boundary))
        print('cell spacing', cells[0].distance(cells[1]))

        self.assertAlmostEqual(cells[0].distance(cells[1]), 0.0)


class TestSquareTile(unittest.TestCase):
    def test_adjacent_tiles_pt1(self):
        """Get some 0.1 degree locations, check we can buld adjacent hexagons."""

        RESOLUTION = 0.1  # degrees / km ???
        grid = load_grid('NZ_0_1_NB_1_1')

        cells = []
        for pt in grid[30:33]:
            cells.append(create_square_tile(RESOLUTION, *pt))

        for cell in cells:
            print(cell.centroid, cell.bounds[2] - cell.bounds[0])

        print('centroid spacing', cells[0].centroid.distance(cells[1].centroid))
        print('cell center to boundary', cells[0].centroid.distance(cells[0].boundary))
        print('cell spacing', cells[0].distance(cells[1]))
        print('cell exterior', list(cells[0].exterior.coords))
        self.assertAlmostEqual(cells[0].distance(cells[1]), 0.0)

    def test_build_geojson_from_squares_pt1(self):

        RESOLUTION = 0.1  # degrees / km ???
        # edge = math.sqrt(RESOLUTION**2/(3/2 * math.sqrt(3)))

        # print(f'edge length {edge}')
        grid = load_grid('NZ_0_1_NB_1_1')

        locs, geometry, values = [], [], []
        for pt in load_grid('NZ_0_1_NB_1_1'):
            locs.append((pt[1], pt[0]))
            geometry.append(create_square_tile(RESOLUTION, pt[1], pt[0]))
            values.append(random.randint(0, 100000))

        gdf = gpd.GeoDataFrame(data=dict(locs=locs, geometry=geometry, values=values))
        self.assertEqual(gdf.shape[0], len(grid))

        # with open('test.json', 'w') as output:
        #     output.write(gdf.to_json())
