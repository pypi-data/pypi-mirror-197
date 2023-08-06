# pyprocessors_gallery

[![license](https://img.shields.io/github/license/oterrier/pyprocessors_gallery)](https://github.com/oterrier/pyprocessors_gallery/blob/master/LICENSE)
[![tests](https://github.com/oterrier/pyprocessors_gallery/workflows/tests/badge.svg)](https://github.com/oterrier/pyprocessors_gallery/actions?query=workflow%3Atests)
[![codecov](https://img.shields.io/codecov/c/github/oterrier/pyprocessors_gallery)](https://codecov.io/gh/oterrier/pyprocessors_gallery)
[![docs](https://img.shields.io/readthedocs/pyprocessors_gallery)](https://pyprocessors_gallery.readthedocs.io)
[![version](https://img.shields.io/pypi/v/pyprocessors_gallery)](https://pypi.org/project/pyprocessors_gallery/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyprocessors_gallery)](https://pypi.org/project/pyprocessors_gallery/)

Multirole to be used as a test gallery for the UI

## Installation

You can simply `pip install pyprocessors_gallery`.

## Developing

### Pre-requesites

You will need to install `flit` (for building the package) and `tox` (for orchestrating testing and documentation building):

```
python3 -m pip install flit tox
```

Clone the repository:

```
git clone https://github.com/oterrier/pyprocessors_gallery
```

### Running the test suite

You can run the full test suite against all supported versions of Python (3.8) with:

```
tox
```

### Building the documentation

You can build the HTML documentation with:

```
tox -e docs
```

The built documentation is available at `docs/_build/index.html.
