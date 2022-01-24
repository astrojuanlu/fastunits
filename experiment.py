import numpy as np

# https://github.com/numpy/numpy-dtypes/tree/main/npytypes/rational
from npytypes.rational import rational as R

from fastunits.dimensions import Dimension
from fastunits.units import Unit
from fastunits.quantities import ScalarQuantity as Quantity

# To experiment, let's stick with TLM
# SI_base = "TLMIϴNJ"
# (Time, Length, Mass, Electric current,
# Thermodynamic temperature, Amount of substance, Luminous intensity)
SI_base = "TLM"


# TODO: Make convenience constructor
T = Dimension(np.array([1, 0, 0], dtype=R), base=SI_base)
L = Dimension(np.array([0, 1, 0], dtype=R), base=SI_base)
M = Dimension(np.array([0, 0, 1], dtype=R), base=SI_base)


m = Unit.base(L, "m")
cm = m.derived(1e-2, "cm")
s = Unit.base(T, "s")
kg = Unit.base(M, "kg")


q1 = 10 << cm
q2 = 1 << m
qq = q1 * q2
qp = q1 + q2

print(q1, q2, qq, qp)

# TODO: np.array([1, 0, 0]) << m does not work as intended
qv1 = Quantity(np.array([1, 0, 0]), m)
qv2 = Quantity(np.array([0, 1, 0]), cm)
qv3 = Quantity(np.random.randn(10_000), m)

# TODO: 2 * qv1 is not implemented
# TODO: Creating dimensionless quantities is difficult

# Promising benchmarks:
# basic arithmetic is ~2x faster than astropy.units,
# quantity creation is ~10x faster than astropy.units.
# composite unit creation is ~1.2x faster than astropy.units.

# This was Step 0
# Step 1: Use faster vector (numpy.array?) and fraction arithmetic (cfractions?) (done)
# stdlib.fractions + Vector gave decent performance, but rational dtype with NumPy arrays was better

# Step 2: Figure out dimensionless quantities (including angles)
# Step 3: Mathematical operations (NumPy ufuncs) including angles (conversion to radians)
# Step 4: Try more micro optimizations (compile with Cython?)
# Step 5: Complete SI units
# Step 6: Different CODATA versions
