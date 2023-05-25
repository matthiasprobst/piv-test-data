import pathlib

import numpy as np
from pivimage import PIVImage

import pivtestdata as ptd

__this_dir__ = pathlib.Path(__file__).parent


def test_vortex_pair():
    vortex_pair = ptd.pivtec.vortex_pair
    assert vortex_pair.name == 'pivtec/vortex_pair'
    assert vortex_pair.url == 'https://www.pivtec.com/download/samples/pivimg1.zip'
    vortex_pair.download()
    assert vortex_pair.image_dir == ptd.user_dir / vortex_pair.name
    assert len(vortex_pair.image_filenames) == 2
    assert isinstance(vortex_pair.A[0], PIVImage)
    assert isinstance(vortex_pair.B[0], PIVImage)


def test_turbulent_bdry_layer():
    turbulent_boundary_layer = ptd.pivtec.turbulent_boundary_layer
    assert turbulent_boundary_layer.name == 'pivtec/turbulent_boundary_layer'
    assert turbulent_boundary_layer.url == 'https://www.pivtec.com/download/samples/pivimg2.zip'
    turbulent_boundary_layer.download()

    assert turbulent_boundary_layer.image_dir == ptd.user_dir / turbulent_boundary_layer.name
    assert len(turbulent_boundary_layer.image_filenames) == 2

    assert isinstance(turbulent_boundary_layer.A[0], PIVImage)
    assert isinstance(turbulent_boundary_layer.B[0], PIVImage)
