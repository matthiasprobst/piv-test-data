import pathlib

import numpy as np

import pivtestdata as ptd

__this_dir__ = pathlib.Path(__file__).parent


def test_vortex_pair():
    vortex_pair = ptd.vortex_pair
    assert vortex_pair.name == 'pivtec/vortex_pair'
    assert vortex_pair.url == 'https://www.pivtec.com/download/samples/pivimg1.zip'
    vortex_pair.download(target_folder=__this_dir__)
    assert vortex_pair.image_dir == __this_dir__ / 'pivtec/vortex_pair'
    assert len(vortex_pair.image_filenames) == 2
    assert vortex_pair.A[0].name == 'A001_1.tif'


def test_turbulent_bdry_layer():
    turbulent_boundary_layer = ptd.turbulent_boundary_layer
    assert turbulent_boundary_layer.name == 'pivtec/turbulent_boundary_layer'
    assert turbulent_boundary_layer.url == 'https://www.pivtec.com/download/samples/pivimg2.zip'
    turbulent_boundary_layer.download(target_folder=__this_dir__)
    assert turbulent_boundary_layer.image_dir == __this_dir__ / 'pivtec/turbulent_boundary_layer'
    assert len(turbulent_boundary_layer.image_filenames) == 2

    assert isinstance(turbulent_boundary_layer.A[0], np.ndarray)
