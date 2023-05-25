import pivtestdata as ptd


def test_version():
    assert ptd.__version__ == '0.2.0'


def test_filesizes():
    assert ptd.pivtec.vortex_pair.file_size == 293629
