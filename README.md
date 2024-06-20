# Welcome to AstroGlue

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/Kam-s18/AstroGlue/ci.yml?branch=main)](https://github.com/Kam-s18/AstroGlue/actions/workflows/ci.yml)
[![Documentation Status](https://readthedocs.org/projects/AstroGlue/badge/)](https://AstroGlue.readthedocs.io/)
[![codecov](https://codecov.io/gh/Kam-s18/AstroGlue/branch/main/graph/badge.svg)](https://codecov.io/gh/Kam-s18/AstroGlue)

## Installation

The Python package `AstroGlue` can be installed from PyPI:

```
python -m pip install AstroGlue
```

## Development installation

If you want to contribute to the development of `AstroGlue`, we recommend
the following editable installation from this repository:

```
git clone https://github.com/Kam-s18/AstroGlue
cd AstroGlue
python -m pip install --editable .[tests]
```

Having done so, the test suite can be run using `pytest`:

```
python -m pytest
```

## Acknowledgments

This repository was set up using the [SSC Cookiecutter for Python Packages](https://github.com/ssciwr/cookiecutter-python-package).
