import pathlib
from dataclasses import dataclass
from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np


def load_img(img_filepath: pathlib.Path):
    """
    loads b16 or other file format
    """
    img_filepath = pathlib.Path(img_filepath)
    if img_filepath.suffix in ('b16', '.b16'):
        try:
            import pco
        except ImportError:
            raise ImportError('Package "pco_tools" missing. you need to install it to load b16 files')
        im_ = pco.load(str(img_filepath))
    else:
        try:
            from cv2 import imread as cv2_imread
        except ImportError:
            raise ImportError('Package "cv2" missing. you need to install it to load b16 files')
        im_ = cv2_imread(str(img_filepath), -1)
    return im_


@dataclass
class PIVImageMetaData:
    """PIV image meta data"""

    # camera characteristics:
    pixel_size_mu: Tuple[float, float] = None  # e.g. (6.7, 6.7); units is micrometer
    sensor_size_mm: Tuple[float, float] = None  #
    dynamic_range_bits: int = None  # e.g. 12; units is bits
    quantum_efficiency: float = None  # e.g. 0.4 for 40%
    full_well_capacity: int = None  # e.g. 25000 e
    readout_noise: int = None  # e.g. 7 e

    field_of_view_m: Tuple[float, float] = None  # e.g. (0.001, 0.001); units is meter

    lens_focal_length_mm: float = None  # e.g. 50; units is millimeter
    lens_f_number: float = None  # e.g. 1.4


class PIVImage(np.ndarray):
    """PIV image array with filename"""

    def __new__(cls, input_array, filename):
        obj = np.asarray(input_array).view(cls)
        obj._filename = filename
        return obj

    @property
    def filename(self):
        """Return filename"""
        return self._filename

    @property
    def name(self):
        """Return filename name"""
        return self.filename.name

    @property
    def stem(self):
        """Return filename stem"""
        return self.filename.stem

    def plot(self, ax=None, **kwargs):
        """Plot image"""
        cmap = kwargs.pop('cmap', 'gray')
        kwargs['cmap'] = cmap
        if ax is None:
            ax = plt.gca()
        ax.imshow(self, **kwargs)
        ax.set_title(self.name)
        return ax


class PIVImages:
    """Collection of PIV images"""

    def __init__(self, filenames: list):
        self.filenames = filenames
        self._images = {}

    def __getitem__(self, item):
        """Return image array"""
        if item not in self._images:
            self._images[item] = load_img(self.filenames[item])
        return PIVImage(self._images[item], filename=self.filenames[item])
