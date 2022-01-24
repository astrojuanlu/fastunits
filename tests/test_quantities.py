import numpy as np
import pytest

from fastunits.dimensions import Dimension
from fastunits.quantities import ScalarQuantity
from fastunits.units import IncommensurableUnitsError, Unit


@pytest.fixture
def unit(dimension):
    return Unit(1.0, dimension, ["a"])


@pytest.fixture
def quantity(unit):
    return ScalarQuantity(1.0, unit)


def test_quantity_to_value_returns_expected_result(quantity):
    input_value = 1.0
    multiplier = 10.0

    derived_unit = quantity.unit.derived(multiplier, ["da"])

    expected_value = input_value / multiplier

    value = quantity.to_value(derived_unit)

    assert value == expected_value


def test_lshift_quantity_creation_from_units_returns_expected_result(unit):
    value = 1.0
    expected_quantity = ScalarQuantity(value, unit)

    quantity = 1.0 << unit

    assert quantity == expected_quantity


def test_quantities_are_equal_to_themselves(quantity):
    assert quantity == quantity


def test_quantities_different_scales_are_equal(quantity):
    input_value = 1.0
    multiplier = 10.0

    derived_unit = quantity.unit.derived(multiplier, ["da"])

    quantity_derived = ScalarQuantity(input_value / multiplier, derived_unit)

    assert quantity_derived == quantity


def test_quantities_different_are_different(quantity):
    q2 = ScalarQuantity(42.0, quantity.unit)

    assert q2 != quantity


def test_quantity_product_returns_expected_result(unit):
    q1 = ScalarQuantity(2.0, unit)
    q2 = ScalarQuantity(3.0, unit)

    expected_q = ScalarQuantity(6.0, unit * unit)

    q = q1 * q2

    assert q == expected_q


def test_quantity_addition_returns_expected_result(unit):
    q1 = ScalarQuantity(2.0, unit)
    q2 = ScalarQuantity(3.0, unit)

    expected_q = ScalarQuantity(5.0, unit)

    q = q1 + q2

    assert q == expected_q


def test_addition_incommensurable_quantities_raises_error(base):
    d1 = Dimension(np.array([1, 0, 0]), base=base)
    d2 = Dimension(np.array([0, 1, 0]), base=base)

    u1 = Unit(1.0, d1, ["a"])
    u2 = Unit(1.0, d2, ["z"])

    q1 = ScalarQuantity(1.0, u1)
    q2 = ScalarQuantity(1.0, u2)

    with pytest.raises(IncommensurableUnitsError, match="Incommensurable quantities"):
        q1 + q2
