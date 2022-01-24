import numpy as np
import pytest

from fastunits.dimensions import Dimension
from fastunits.quantities import IncommensurableUnitsError, Quantity
from fastunits.units import Unit


@pytest.fixture
def unit(dimension):
    return Unit(1.0, dimension, ["a"])


@pytest.fixture
def quantity(unit):
    return Quantity(1.0, unit)


def test_quantity_to_value_returns_expected_result(quantity):
    input_value = 1.0
    multiplier = 10.0

    derived_unit = quantity.unit.derived(multiplier, ["da"])

    expected_value = input_value / multiplier

    value = quantity.to_value(derived_unit)

    assert value == expected_value


def test_quantities_are_equal_to_themselves(quantity):
    assert quantity == quantity


def test_quantities_different_scales_are_equal(quantity):
    input_value = 1.0
    multiplier = 10.0

    derived_unit = quantity.unit.derived(multiplier, ["da"])

    quantity_derived = Quantity(input_value / multiplier, derived_unit)

    assert quantity_derived == quantity


def test_quantities_different_are_different(quantity):
    q2 = Quantity(42.0, quantity.unit)

    assert q2 != quantity


def test_quantity_product_returns_expected_result(unit):
    q1 = Quantity(2.0, unit)
    q2 = Quantity(3.0, unit)

    expected_q = Quantity(6.0, unit * unit)

    q = q1 * q2

    assert q == expected_q


def test_quantity_addition_returns_expected_result(unit):
    q1 = Quantity(2.0, unit)
    q2 = Quantity(3.0, unit)

    expected_q = Quantity(5.0, unit)

    q = q1 + q2

    assert q == expected_q


def test_addition_incommensurable_quantities_raises_error(base):
    d1 = Dimension(np.array([1, 0, 0]), base=base)
    d2 = Dimension(np.array([0, 1, 0]), base=base)

    u1 = Unit(1.0, d1, ["a"])
    u2 = Unit(1.0, d2, ["z"])

    q1 = Quantity(1.0, u1)
    q2 = Quantity(1.0, u2)

    with pytest.raises(IncommensurableUnitsError, match="Incommensurable quantities"):
        q1 + q2
