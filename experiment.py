import numpy as np

from npytypes.rational import rational as R

# To experiment, let's stick with TLM
# SI_base = "TLMIϴNJ"
# (Time, Length, Mass, Electric current,
# Thermodynamic temperature, Amount of substance, Luminous intensity)
SI_base = "TLM"


# Dimensions form a vector space
class Dimension:
    def __init__(self, vector, base=SI_base):
        assert len(vector) == len(base)
        self._vector = vector
        self._base = SI_base

    def __mul__(self, other):
        return Dimension(self._vector + other._vector)

    def __pow__(self, other):
        return Dimension(R(other) * self._vector)

    def __repr__(self):
        fragments = []
        for index, exponent in enumerate(self._vector):
            fragments.append(f"{self._base[index]}({exponent})")
        # TODO: Use Unicode superscripts instead of parenthesis
        # TODO: Reuse this logic for units presentation
        return "".join(fragments) if fragments else "(0)"

    def __eq__(self, other):
        return (self._vector == other._vector).all() and (self._base == other._base)


# TODO: Make convenience constructor
T = Dimension(np.array([1, 0, 0], dtype=R))
L = Dimension(np.array([0, 1, 0], dtype=R))
M = Dimension(np.array([0, 0, 1], dtype=R))


# To relate each unit with the others,
# we introduce the concept of "magnitude",
# which will be unitary for fundamental units in the system
# Notice that we use the same class for simple units and for composite units
class Unit:
    def __init__(self, magnitude, dimensions, names):
        self._magnitude = magnitude
        self._dimensions = dimensions
        self._names = names

    @classmethod
    def derived(cls, relative_magnitude, other, names):
        return cls(relative_magnitude * other._magnitude, other._dimensions, names)

    def __repr__(self):
        return f"{'·'.join(n for n in self._names)}"

    def __mul__(self, other):
        return Unit(
            self._magnitude * other._magnitude,
            self._dimensions * other._dimensions,
            self._names + other._names,
        )

    def __pow__(self, other):
        return Unit(
            self._magnitude ** other,
            self._dimensions ** other,
            [f"{n}{R(other)}" for n in self._names],
        )

    def __truediv__(self, other):
        return Unit(
            self._magnitude / other._magnitude,
            self._dimensions * other._dimensions ** -1,
            self._names + [f"{n}-1" for n in other._names],
        )

    def __rlshift__(self, other):
        # This implements number << unit for easy Quantity creation
        if hasattr(other, "__len__"):
            # NOTE: Explicit dependency with NumPy,
            # should we make this more generic?
            # Or is it enough to provide a convenience constructor?
            # Should we use np.asarray instead?
            other = np.array(other)
        return Quantity(other, self)


m = Unit(1, L, ["m"])
cm = Unit.derived(1e-2, m, ["cm"])
s = Unit(1, T, ["s"])
kg = Unit(1, M, ["kg"])


# Each quantity is a value with a unit
class Quantity:
    def __init__(self, value, unit):
        self._value = value
        self._unit = unit

    def __repr__(self):
        return f"{self._value} {self._unit}"

    def __mul__(self, other):
        return Quantity(self._value * other._value, self._unit * other._unit)

    def __add__(self, other):
        # The line below will fail if the magnitudes are incommensurable
        other_converted_value = other.to_value(self._unit)
        return Quantity(self._value + other_converted_value, self._unit)

    def to_value(self, unit):
        if unit._dimensions != self._unit._dimensions:
            raise ValueError("Incommensurable quantities")
        return (self._unit._magnitude / unit._magnitude) * self._value

    def to(self, unit):
        return Quantity(self.to_value(unit), unit)


q1 = 10 << cm
q2 = 1 << m
qq = q1 * q2
qp = q1 + q2

print(q1, q2, qq, qp)

qv1 = [1, 0, 0] << m
qv2 = [0, 1, 0] << cm

# TODO: np.array([1, 0, 0]) << m does not work as intended
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