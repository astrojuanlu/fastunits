from __future__ import annotations

from fractions import Fraction
from typing import Type, TypeVar

from .dimensions import Dimension

T = TypeVar("T", bound="Unit")


# To relate each unit with the others,
# we introduce the concept of "magnitude",
# which will be unitary for fundamental units in the system
# Notice that we use the same class for simple units and for composite units
class Unit:
    def __init__(self, magnitude: float, dimensions: Dimension, names: list[str]):
        self._magnitude = magnitude
        self._dimensions = dimensions
        self._names = names

    @classmethod
    def derived(
        cls: Type[T], other: T, relative_magnitude: float, names: list[str]
    ) -> T:
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
            [f"{n}{Fraction(other)}" for n in self._names],  # TODO: Rewrite
        )

    def __truediv__(self, other):
        return Unit(
            self._magnitude / other._magnitude,
            self._dimensions * other._dimensions ** -1,
            self._names + [f"{n}-1" for n in other._names],
        )

    def __eq__(self, other):
        # NOTE: This compares magnitudes exactly even if they are floating point values,
        # since we are checking for exact equality
        return (
            (self._magnitude == other._magnitude)
            and (self._dimensions == other._dimensions)
            and (self._names == other._names)
        )
