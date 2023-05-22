import pathlib
import re
import warnings
import zipfile
from dataclasses import dataclass
from typing import Tuple

import appdirs
import requests
from tqdm import tqdm

user_dir = pathlib.Path(appdirs.user_data_dir('pivtestdata'))

# IMG_EXTENSIONS = ('.tif', '.tiff', '.b16')
IMG_FILE_PATTERN = r'^(?!.*mask).*\.(tif|tiff|b16|bmp)$'
MASK_FILE_PATTERN = r'^(.*mask).*\.(tif|tiff|b16|bmp)$'


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


class PIVImages:

    def __init__(self, filenames: list):
        self.filenames = filenames
        self._images = {}

    def __getitem__(self, item):
        """Return image array"""
        if item not in self._images:
            self._images[item] = load_img(self.filenames[item])
        return self._images[item]


class WebZip:
    """Web resource as zip file"""

    def __init__(self, url: str, name=None):
        self.url = url

        if name is None:
            self.name = pathlib.Path(self.url).stem
        else:
            self.name = name

        self.image_dir = None  # can also be used as flag if the dataset is downloaded
        self._all_files = None
        self._meta = PIVImageMetaData()

    def __repr__(self):
        return f'{self.__class__.__name__}(name={self.name}, url={self.url})'

    @property
    def file_size(self):
        """Return file size in bytes"""
        r = requests.get(self.url, stream=True)
        return int(r.headers.get("content-length", 0))

    def download(self, target_folder: pathlib.Path = None):
        """download to user dir or specified target folder"""
        if target_folder is None:
            target_folder = user_dir

        target_folder = target_folder / self.name

        if target_folder.exists():
            # TODO: better check if all images are there. For this we need to know what to expect
            self.image_dir = target_folder
            return target_folder
        else:
            target_folder.mkdir(parents=True)
        zip_filename = target_folder / 'file.zip'
        try:
            r = requests.get(self.url, stream=True)
            total_size = int(r.headers.get("content-length", 0))
            with open(zip_filename, "wb") as file, tqdm(total=total_size, unit='B', unit_scale=True,
                                                        desc=self.name) as progress_bar:
                for data in r.iter_content(chunk_size=1024):
                    # Write the data to the file
                    file.write(data)
                    progress_bar.update(len(data))

            with zipfile.ZipFile(zip_filename) as z:
                z.extractall(target_folder)
            self.image_dir = target_folder
            zip_filename.unlink()
        except Exception as e:
            print(f'could not download {self.name} from {self.url}: {e}')

        return target_folder

    @property
    def all_files(self):
        """return all files in the dataset"""
        if self.image_dir is None:
            raise ValueError('download the dataset first')
        if self._all_files is None:
            self._all_files = sorted(pathlib.Path(self.image_dir).glob('*.*'))
        return self._all_files

    @property
    def image_filenames(self):
        """return all image filenames in the dataset"""
        return sorted([f for f in self.all_files if re.match(IMG_FILE_PATTERN, f.name, re.IGNORECASE)])

    @property
    def mask_filename(self):
        """return the mask filename in the dataset"""
        return sorted([f for f in self.all_files if re.match(MASK_FILE_PATTERN, f.name, re.IGNORECASE)])

    @property
    def readme(self) -> str:
        """Return the content of the readme file as string"""
        if self.image_dir is None:
            raise ValueError('download the dataset first')
        # guess the readme file: use regex for this on file names:
        all_files = pathlib.Path(self.image_dir).glob('*.*')
        readme_file_candidates = [f for f in all_files if re.match(r'readme', f.name, re.IGNORECASE)]
        readme = readme_file_candidates[0]
        if len(readme_file_candidates) == 1:
            warnings.warn(f'found multiple readme files. Will use {readme}. Others are: {readme_file_candidates}',
                          UserWarning)
        return readme.read_text()

    @property
    def meta(self) -> PIVImageMetaData:
        return self._meta

    @property
    def A(self):
        """Return image A interface class"""
        return PIVImages(filenames=self.image_filenames[::2])

    @property
    def B(self):
        """Return image B interface class"""
        return PIVImages(filenames=self.image_filenames[::2])
