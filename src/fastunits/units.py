from __future__ import annotations

from fractions import Fraction
from typing import Type, TypeVar

from .dimensions import Dimension

_T = TypeVar("_T", bound="Unit")


class IncommensurableUnitsError(ValueError):
    pass


# To relate each unit with the others,
# we introduce the concept of "magnitude",
# which will be unitary for fundamental units in the system
# Notice that we use the same class for simple units and for composite units
class Unit:

    # Trick to make `np.array([...]) << unit` work,
    # borrowed from https://github.com/astropy/astropy/blob/d1e122d/\
    # astropy/units/core.py#L630-L632
    __array_priority__ = 1001

    def __init__(self, magnitude: float, dimensions: Dimension, names: list[str]):
        self._magnitude = magnitude
        self._dimensions = dimensions
        self._names = names

    @classmethod
    def base(cls: Type[_T], dimensions: Dimension, name: str) -> _T:
        # The magnitude of base units is not important,
        # what's important is the relative magnitude of derived units,
        # hence we hardcode 1.0
        return cls(1.0, dimensions, [name])

    def derived(self: _T, relative_magnitude: float, name: str) -> _T:
        return self.__class__(
            relative_magnitude * self._magnitude, self._dimensions, [name]
        )

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
            [f"{n}{Fraction(other)}" for n in self._names],  # TODO: Rewrite
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
            from .quantities import ArrayQuantity

            return ArrayQuantity.from_list(other, self)
        else:
            from .quantities import ScalarQuantity

            return ScalarQuantity(other, self)

    def __eq__(self, other):
        # NOTE: This compares magnitudes exactly even if they are floating point values,
        # since we are checking for exact equality
        return (
            (self._magnitude == other._magnitude)
            and (self._dimensions == other._dimensions)
            and (self._names == other._names)
        )
