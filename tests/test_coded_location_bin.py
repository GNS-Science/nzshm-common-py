from collections import OrderedDict

from nzshm_common import grids
from nzshm_common.location.code_location import CodedLocationBin, bin_locations

GRID_LOCS = grids.get_location_grid("NZ_0_1_NB_1_0", resolution=0.1)
GRID_LOCS_EXPECTED_BIN_COUNT_05 = 196


def test_coded_location_bin_empty():
    single_bin = CodedLocationBin(GRID_LOCS, bin_resolution=1)
    assert len(single_bin.locations) == 0, "A bin can be instantiated with no locations in it"


def test_coded_location_binning_nosort():
    """
    A collection of bins can be left unsorted.
    """
    grid_bins = bin_locations(GRID_LOCS, at_resolution=0.5, sort_bins=False)
    assert isinstance(grid_bins, OrderedDict), "Bin collection should be ordered dictionary"
    assert len(grid_bins) == GRID_LOCS_EXPECTED_BIN_COUNT_05, "Bin count should match expectation"

    first_loc = GRID_LOCS[0]
    expected_first_bin_key = first_loc.downsample(0.5).code
    first_bin_key = list(grid_bins.keys())[0]
    assert first_bin_key == expected_first_bin_key, "First bin should match the downsampled code of the first location"

    first_bin = grid_bins[first_bin_key]
    assert isinstance(first_bin, CodedLocationBin), "Should be CodedLocationBin"
    assert len(first_bin) == len(first_bin.locations), "__len__ should reflect locations list length"
    assert first_bin.locations[0] == first_loc, "Unsorted, first location should be first item in the first bin"

    all_bin_counts = [len(grid_bin) for grid_bin in grid_bins.values()]
    assert sum(all_bin_counts) == len(GRID_LOCS), "Bin counts should sum to total location count"

    assert first_bin.locations == [loc for loc in first_bin], "Bin __iter__ should match its locations list"


def test_coded_location_binning_sort():
    """
    A collection of bins should be sorted geographically by default.
    """
    grid_bins = bin_locations(GRID_LOCS, at_resolution=0.5)

    assert isinstance(grid_bins, OrderedDict), "Bin collection should be ordered dictionary"
    assert len(grid_bins) == GRID_LOCS_EXPECTED_BIN_COUNT_05, "Bin count should match expectation"

    bin_list = list(grid_bins.values())
    min_bin = min(bin_list, key=lambda b: b.reference_point)
    max_bin = max(bin_list, key=lambda b: b.reference_point)

    assert min_bin == bin_list[0], "'Smallest' bin should be first"
    assert grid_bins[min_bin.code] == min_bin
    assert max_bin == bin_list[-1], "'Largest' bin should be last"
    assert grid_bins[max_bin.code] == max_bin

    assert min_bin.locations == sorted(min_bin.locations), "Bin locations should be sorted"
    assert min_bin.locations == sorted([loc for loc in min_bin])

    print()
    print("NW-most bin:", min_bin)
    print("SE-most bin:", max_bin)
