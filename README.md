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

### Mathematical theory of dimensions

- https://terrytao.wordpress.com/2012/12/29/a-mathematical-formalisation-of-dimensional-analysis/
- https://math.stackexchange.com/q/3483152/24849
- https://mathoverflow.net/q/402497

### Angles as separate dimension

- https://www.physicsforums.com/insights/can-angles-assigned-dimension/
- "Implications of adopting plane angle as a base quantity in the SI" https://doi.org/10.1088/0026-1394/53/3/998
- "Physical Entities and Mathematical Representation" https://doi.org/10.1109/IRET-MIL.1962.5008463
- https://physics.stackexchange.com/q/252288/7641
- https://physics.stackexchange.com/q/33542/7641

### Units with offsets

- Not as easy as it looks! https://github.com/astropy/astropy/pull/2209/
- Actually, much more difficult than it looks! https://pint.readthedocs.io/en/latest/nonmult.html
- unyt also gives up https://github.com/yt-project/unyt/blob/b9c4c21b2e27fd4af9fafa1949dc01296125543c/unyt/unit_object.py#L411-L421

### Interoperability with NumPy

tl;dr: fastunits should provide its own compatibility layer on top of the Array API,
to maintain a simple and hackable implementation that can work with many array containers.

The big question is: should `np.add(q1, q2)` return a fastunits Quantity object?
And it turns out that this has lots of ramifications.

_[Thread in scientific-python about these topics](https://discuss.scientific-python.org/t/advice-and-guidance-about-array-api-for-a-units-package/336?u=astrojuanlu)_

There are several methods currently available to extend or interface with NumPy,
and proposals to add a few more.
However, reading the original NumPy Enhancement Proposals (NEPs for short)
is not always helpful to understand the historical evolution of a particular method:
this information is instead captured in newer documents or GitHub threads
that look back on past proposals and evaluate their adoption.

For example, the introduction of NEP 37 "A dispatch protocol for NumPy-like modules" (draft, 2019)
mentions several drawbacks to NEP 18 `__array_function__` protocol (final, 2018)
that were only discovered after libraries tried to adopt it.
One of them is backwards compatibility: NEP 18 says

> There are no general requirements on the return value from `__array_function__`,
> although most sensible implementations should probably return array(s)
> with the same type as one of the function's arguments.

However, NEP 37 recollects

> `__array_function__` has significant implications for libraries that use it:
> [...] users expect NumPy functions like np.concatenate to return NumPy arrays.
> [...] Libraries like Dask and CuPy have looked at and accepted
> the backwards incompatibility impact of `__array_function__`;
> it would still have been better for them if that impact didn't exist".

This suggests that `np.sum(q1, q2)` returning an object that is _not_ a NumPy array
proved to be contentious or problematic for some downstream users.
`astropy.units` should in principle not be affected by this problem
since their `Quantity` objects inherit `numpy.ndarray`,
however it would be useful to determine whether the incompatibilities of `astropy.units`
with Dask and xarray summarized in https://github.com/astropy/astropy/issues/12600#issuecomment-1003044555
come from this design decision.

On the other hand, the unyt project described some challenges of implementing `__array_function__`
in https://github.com/yt-project/unyt/issues/139. In particular,
unyt seems to be affected by what NEP 37 called "an all or nothing approach" or
"no good pathway for incremental adoption", and in addition
there is not an official listing of NumPy functions supporting `__array_function__`
as requested in https://github.com/numpy/numpy/issues/15544.
All these challenges are not necessarily technical barriers,
but increase the amount of work needed to properly adopt `__array_function__`.

The difficulties stated above seem a bit discouraging,
and so maybe fastunits could experiment with an alternative approach:
rather than treating Quantity objects like NumPy arrays (by establishing a direct inheritance relationship)
or even like a provider of an Array API https://data-apis.org/array-api/latest/,
fastunits could implement Quantity objects as _containers_ of array types,
hence becoming an "array consumer library" as depicted in https://github.com/data-apis/array-api/issues/1.
If done properly, this should enable fastunits to work not only with NumPy arrays as data containers,
but also with Dask arrays, CuPy arrays,
or virtually any other library implementing the Python array API standard.

Going back to the original question (what should something like `np.add(q1, q2)` return?)
we could imagine something like this:

```python
def quantity_add(q1, q2):
    # Check that q1 and q2 are commensurable, and if so,
    unit = q1._unit

    # These values can be any array type!
    v1 = q1._value
    v2 = q2._value

    # Retrieve Array API namespace, see NEP 47
    xp = get_namespace(v1, v2)

    # Apply target function from loaded namespace
    v_add = xp.add(v1, v2)

    # Create new Quantity from that
    return Quantity(v_add, unit)
```

The disadvantage is that users would not be able to just call `np.add(q1, q2)`
and receive a fastunits Quantity, forcing them to do something like

```
import fastunits.numpy_compat as funp

q = funp.sum(q1, q2)
```

In return, we would get these advantages:

- fastunits can gradually increase the coverage of the Array API.
  This, in turn, creates a point for easy contributions.
- fastunits should be able to work with any array provider,
  deferring all array operations to the underlying container.

Would users of Dask, CuPy and the like be satisfied by this solution?
It can be argued that they have no other option,
since the existing physical unit libraries are not extensible enough.
On the other hand, maybe there exists some better solution that could be achieved by a better design,
but at the moment that lives on the realm of "unknown unknowns".

As it happened with NumPy `__array_function__` and others, there is only one way to know:
putting the code on the users hands.
