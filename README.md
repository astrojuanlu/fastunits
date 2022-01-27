# fastunits

[![Documentation Status](https://readthedocs.org/projects/fastunits/badge/?version=latest)](https://fastunits.readthedocs.io/en/latest/?badge=latest)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![PyPI](https://img.shields.io/pypi/v/fastunits)](https://pypi.org/project/fastunits)

A fast physical units library compatible with NumPy

## Installation

To install, run

```
(.venv) $ pip install fastunits
```

## Overview

Add a longer description here.

## Notes

- NumPy compatibility
- Different unit systems (CODATA versioned constants), should be easy to
  swap them and make calculations between them
- Seven dimensions: time, length, mass, electric current, thermodynamic temperature,
  amount of substance, luminous intensity
  - Angles are derived units in m/m
- See https://github.com/tbekolay/quantities-comparison !
- See also https://mpusz.github.io/wg21-papers/papers/1935R0_a_cpp_approach_to_physical_units.html especially ISO 80000-1:2009(E)
- Inspiration
  - ndindex benchmarks https://quansight-labs.github.io/ndindex/benchmarks/
    - Remember affordable dedicated servers https://www.kimsufi.com
    - Alternatively, use something like https://github.com/marketplace/actions/continuous-benchmark,
      which depends on pytest-benchmark
      - And don't lose sight of https://github.com/pandas-dev/pandas/issues/45049 and https://github.com/rapidsai/asvdb
  - ndindex optional cythonization https://github.com/Quansight-Labs/ndindex/pull/127
  - sgp4 optional extension https://github.com/brandon-rhodes/python-sgp4/blob/master/setup.py
  - PyO3 rust-numpy https://github.com/PyO3/rust-numpy
