from nzshm_common import location


def test_location_keys_unique():
    assert len(location.LOCATIONS) == len(set(loc['id'] for loc in location.LOCATIONS))

def test_location_lists():
    assert len(location.LOCATION_LISTS["NZ"]["locations"]) == 36
    assert len(location.LOCATION_LISTS["SRWG214"]["locations"]) == 214
    assert len(location.LOCATION_LISTS["ALL"]["locations"]) == 214 + 36

def test_location_rot():
    rot = location.LOCATIONS_BY_ID['ROT']
    assert rot['name'] == 'Rotorua'

def test_location_pauanui():
    rot = location.LOCATIONS_BY_ID['srg_34']
    assert rot['name'] == 'Pauanui'