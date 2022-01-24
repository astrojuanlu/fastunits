from __future__ import annotations

from typing import Any

from .units import Unit


class IncommensurableUnitsError(ValueError):
    pass


# Each quantity is a value with a unit
class _BaseQuantity:
    def __init__(self, value: Any, unit: Unit):
        self._value = value
        self._unit = unit

    @property
    def unit(self):
        return self._unit

    def __repr__(self):
        return f"{self._value} {self._unit}"

    def __mul__(self, other):
        return self.__class__(self._value * other._value, self._unit * other._unit)

    def __add__(self, other):
        # The line below will fail if the magnitudes are incommensurable
        other_converted_value = other.to_value(self._unit)
        return self.__class__(self._value + other_converted_value, self._unit)

    def to_value(self, unit: Unit) -> Any:
        if unit._dimensions != self._unit._dimensions:
            raise IncommensurableUnitsError("Incommensurable quantities")
        return (self._unit._magnitude / unit._magnitude) * self._value

    def to(self, unit):
        return self.__class__(self.to_value(unit), unit)


class ScalarQuantity(_BaseQuantity):
    def __init__(self, value: float, unit: Unit):
        super().__init__(value, unit)

    def __eq__(self, other):
        return self.exactly_equal(other) or self.exactly_equal(other.to(self.unit))

    def exactly_equal(self, other: _BaseQuantity) -> bool:
        return bool((self.unit == other.unit) and (self._value == other._value))
