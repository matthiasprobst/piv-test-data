import pathlib

import pivtestdata as ptd

__this_dir__ = pathlib.Path(__file__).parent


def test_pivchallenge_meta():
    assert ptd.piv_challenge.pc_1A.meta.pixel_size_mu == (6.7, 6.7)


def test_pivchallenge():
    n_imgs = (2, 12, 4, 16)
    for case_name, n_img in zip(('A', 'B', 'C', 'E'), n_imgs):
        pc1 = ptd.piv_challenge[1][case_name]
        assert pc1.name == f'piv_challenge/1/{case_name}'
        assert pc1.url == f'https://www.pivchallenge.org/pub/{case_name}/{case_name}.zip'
        assert pc1.challenge_number == 1
        assert pc1.case == case_name
        assert pc1.image_dir is None
        pc1.download(target_folder=__this_dir__)
        assert pc1.image_dir == __this_dir__ / f'piv_challenge/1/{case_name}'
        assert len(pc1.image_filenames) == n_img
        # assert pc1.image_filenames[0].name == 'A001_1.tif'
        # assert pc1.image_filenames[1].name == 'A001_2.tif'


def test_pivchallenge_2():
    n_imgs = (200, 200, 200)
    for case_name, n_img in zip(('A', 'B', 'C'), n_imgs):
        pc1 = ptd.piv_challenge[2][case_name]
        assert pc1.name == f'piv_challenge/2/{case_name}'
        assert pc1.url == f'https://www.pivchallenge.org/pub03/{case_name}all.zip'
        assert pc1.challenge_number == 2
        assert pc1.case == case_name
        assert pc1.image_dir is None
        pc1.download(target_folder=__this_dir__)
        assert pc1.image_dir == __this_dir__ / f'piv_challenge/2/{case_name}'
        assert len(pc1.image_filenames) == n_img
        # assert pc1.image_filenames[0].name == 'A001_1.tif'
        # assert pc1.image_filenames[1].name == 'A001_2.tif'
