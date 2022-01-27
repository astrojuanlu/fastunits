from __future__ import annotations

from typing import Sequence, Type, TypeVar

import numpy as np
from npytypes.rational import rational as R
from numpy.typing import NDArray

# Seven base dimensions in the SI: Time, Length, Mass, Electric current,
# Thermodynamic temperature, Amount of substance, Luminous intensity
SI_base = "TLMIϴNJ"


def dimensions_from_base(base: Sequence[str]) -> tuple[Dimension, ...]:
    dimensions = []  # list[Dimension]
    for dimension_name in base:
        dimensions.append(Dimension.create(dimension_name, base=base))

    return tuple(dimensions)


_D = TypeVar("_D", bound="Dimension")


# Dimensions form a vector space
class Dimension:
    def __init__(self, vector: NDArray[R], base: Sequence[str]):
        self._vector = vector
        self._base = base

    @classmethod
    def create(cls: Type[_D], name: str, base: Sequence[str]) -> _D:
        # This will raise a ValueError if `name` not found in `base`
        position = base.index(name)

        vector = np.zeros(len(base), dtype=R)
        vector[position] = 1

        return cls(vector, base)

    def __mul__(self, other):
        assert self._base is other._base
        return Dimension(self._vector + other._vector, self._base)

    def __pow__(self, other):
        return Dimension(R(other) * self._vector, self._base)

    def __repr__(self):
        fragments = []
        for index, exponent in enumerate(self._vector):
            fragments.append(f"{self._base[index]}({exponent})")
        # TODO: Use Unicode superscripts instead of parenthesis
        # TODO: Reuse this logic for units presentation
        return "".join(fragments) if fragments else "(0)"

    def __eq__(self, other):
        return (self._vector == other._vector).all() and (self._base == other._base)
