import numpy as np

from fastunits.dimensions import dimensions_from_base
from fastunits.units import Unit
from fastunits.quantities import ScalarQuantity, ArrayQuantity

# To experiment, let's stick with TLM
T, L, M, U = dimensions_from_base("TLM")

m = Unit.base(L, "m")
cm = m.derived(1e-2, "cm")

s = Unit.base(T, "s")

kg = Unit.base(M, "kg")

rad = Unit.from_unit(m / m, "rad")
deg = rad.derived(np.pi / 180, "°")

one = dimensionless_unscaled = Unit.base(U, "")


a = 1 << rad
print(a, a.to(deg))

b = 1 << one
print(b, b + (2 << one))

q1 = 10 << cm
q2 = 1 << m
qq = q1 * q2
qp = q1 + q2
print(q1, q2, qq, qp)

qv1 = [1, 0, 0] << m
qv2 = [0, 1, 0] << cm
qv3 = np.random.randn(10_000) << m
print(qv1 + qv2)

print(2 * qv1)
# print(qv1 * 2)  # Not implemented to reduce complexity

# Promising benchmarks:
# basic arithmetic is ~2x faster than astropy.units,
# quantity creation is ~10x faster than astropy.units.
# composite unit creation is ~1.2x faster than astropy.units.

# This was Step 0
# Step 1: Use faster vector (numpy.array?) and fraction arithmetic (cfractions?) (done)
# stdlib.fractions + Vector gave decent performance, but rational dtype with NumPy arrays was better
# Step 2: Figure out dimensionless quantities (including angles)
# angles as dimensionless quantities is a bit of a mess https://doi.org/10.1088/0026-1394/53/3/998
# we choose not to take a stance

# Step 3: Mathematical operations (NumPy ufuncs) including angles (conversion to radians)
# Step 4: Try more micro optimizations (compile with Cython?)
# Step 5: Complete SI units
# Step 6: Different CODATA versions
