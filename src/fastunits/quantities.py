from __future__ import annotations

from typing import Any, Sequence, Type, TypeVar

import numpy as np
from numpy.typing import NBitBase, NDArray

from .units import IncommensurableUnitsError, Unit

_T = TypeVar("_T", bound="_BaseQuantity")


# Each quantity is a value with a unit
class _BaseQuantity:
    def __init__(self, value: Any, unit: Unit):
        self._value = value
        self._unit = unit

    @property
    def unit(self):
        return self._unit

    def __repr__(self):
        suffix = str(self._unit)
        return f"{self._value} {suffix}" if suffix else f"{self._value}"

    def __mul__(self, other):
        return self.__class__(self._value * other._value, self._unit * other._unit)

    def __rmul__(self, other):
        # Assume other is a number
        return self.__class__(self._value * other, self._unit)

    def __add__(self, other):
        # The line below will fail if the magnitudes are incommensurable
        other_converted_value = other.to_value(self._unit)
        return self.__class__(self._value + other_converted_value, self._unit)

    def to_value(self, unit: Unit) -> Any:
        if unit._dimensions != self._unit._dimensions:
            raise IncommensurableUnitsError("Incommensurable quantities")

        # TODO: Move multiplicative factor logic to Unit class,
        # so that more complex logic can be implemented?
        # However, that would create another layer of indirection
        # (possibly with a small impact in performance)
        # only to support non-multiplicative units
        # like temperature scales (Celsius, Fahrenheit, and the like)
        return (self._unit._multiplier / unit._multiplier) * self._value

    def to(self: _T, unit: Unit) -> _T:
        return self.__class__(self.to_value(unit), unit)


class ScalarQuantity(_BaseQuantity):
    def __init__(self, value: float, unit: Unit):
        super().__init__(value, unit)

    def __eq__(self, other):
        return self.exactly_equal(other) or self.exactly_equal(other.to(self.unit))

    def exactly_equal(self, other: _BaseQuantity) -> bool:
        return bool((self.unit == other.unit) and (self._value == other._value))


_TA = TypeVar("_TA", bound="ArrayQuantity")
_P = TypeVar("_P", bound=NBitBase)


class ArrayQuantity(_BaseQuantity):
    def __init__(self, value: NDArray[np.number[_P]], unit: Unit):
        super().__init__(value, unit)

    @classmethod
    def from_list(cls: Type[_TA], values: Sequence[float], unit: Unit) -> _TA:
        # TODO: Should we go beyond np.asarray?
        # See https://numpy.org/neps/nep-0047-array-api-standard.html\
        # #the-asarray-asanyarray-pattern
        return cls(np.asarray(values), unit)

    def equals_exact(self, other: _BaseQuantity) -> bool:
        return (self.unit == other.unit) and bool((self._value == other._value).all())

    def is_equivalent_exact(self, other: _BaseQuantity) -> bool:
        return self.equals_exact(other) or self.equals_exact(other.to(self.unit))
