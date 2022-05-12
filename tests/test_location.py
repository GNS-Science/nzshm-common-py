from nzshm_common import location

def test_location_keys_unique():
	assert len(location.LOCATIONS) == len(set(loc['id'] for loc in location.LOCATIONS))