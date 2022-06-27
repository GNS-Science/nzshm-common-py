from nzshm_common.grids.region_grid import load_grid


def test_load_wlg_0_005():
    assert len(load_grid('WLG_0_05_nb_1_1')) == 62


def test_load_wlg_0_001():
    assert len(load_grid('WLG_0_01_nb_1_1')) == 764

