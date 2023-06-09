# PIV Test Data

This repository provides test data which is freely available on the internet, so all credit goes to the original
authors. Available data sets are:

* [PIV Challenge 2001](https://www.pivchallenge.org/)
* [ILA Vortex PAIR](https://www.pivtec.com/pivview.html)

Use this repo to test your PIV algorithms.

Note, that the data is not stored in this repo but it assists in downloading it from the respective websites on demand.
Once downloaded, the repo helps you to retrieve the file names quickly or even to load the images into memory.

## Installation

You can install this package via:

```bash
pip install git+https://github.com/matthiasprobst/piv-test-data.git
```

## Usage

Minimal example (for more see the [notebook](notebooks/usage.ipynb)):

```python
import pivtestdata as ptd

case = ptd.piv_challenge.pc_1A

print('File size: ', case.file_size)  # will return the file size in bytes
case.download()  # will download the data if not already present

# get the image (numpy) arrays:
imgA0 = case.A[0]
imgB0 = case.B[0]

print(case.info)  # will return the README content of the case

imgA0.plot()  # plot image A
```

Note, the following cases are available for the various PIV Challenges (PC) upon some are quite large and take a while
to download (Especially cases 3 and 4, use `.file_size` to check the file size before downloading):

PC # | Cases
--- | ---
1 | A, B, C, E
2 | A, B, C
3 | A, B, C
4 | A, B, C, D, E, F

## ToDo

add the [Japanese standard images](http://www.vsj.jp/~pivstd/image-e.html)