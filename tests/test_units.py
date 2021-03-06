import pytest

from fastunits.units import Unit, _Dimensionless


@pytest.fixture
def unit(dimension):
    return Unit.base(dimension, "a")


def test_units_are_equal_to_themselves(unit):
    assert unit == unit


def test_unit_base_returns_expected_result(dimension):
    expected_unit = Unit(1.0, dimension, ["a"])

    unit = Unit.base(dimension, "a")

    assert unit == expected_unit


def test_unit_dimensionless_returns_expected_result(dimension):
    expected_unit = Unit(1.0, dimension ** 0, [_Dimensionless.DIMENSIONLESS])
    expected_str = "(dimensionless)"

    unit = Unit.dimensionless(dimension)

    assert unit == expected_unit
    assert str(unit) == expected_str


def test_unit_derived_returns_expected_result(dimension):
    unit_base = Unit.base(dimension, "a")
    unit_d = unit_base.derived(10, "da")
    expected_unit = Unit(10, dimension, ["da"])

    assert unit_d == expected_unit


def test_unit_from_unit_returns_expected_result(dimension):
    unit_base = Unit.base(dimension, "a")
    unit_d = Unit.from_unit(unit_base, "b")
    expected_unit = Unit(1.0, dimension, ["b"])

    assert unit_d == expected_unit


def test_unit_product_returns_expected_result(dimension):
    unit1 = Unit(1.0, dimension, ["a"])
    unit2 = Unit(2.0, dimension, ["b"])

    expected_composite_unit = Unit(2.0, dimension * dimension, ["a", "b"])

    unit_prod = unit1 * unit2

    assert unit_prod == expected_composite_unit


def test_unit_product_same_unit_returns_expected_result(dimension):
    # This test is here to make explicit that
    # str(a * a) != str(a ** 2)
    # although it's not clear to me whether we should change the behavior?
    unit = Unit(1.0, dimension, ["a"])
    expected_composite_unit = Unit(1.0, dimension * dimension, ["a", "a"])

    unit_prod = unit * unit

    assert unit_prod == expected_composite_unit


def test_unit_power_returns_expected_result(dimension):
    unit = Unit(2.0, dimension, ["a"])
    expected_unit = Unit(4.0, dimension * dimension, ["a²"])

    unit_pow = unit ** 2

    assert unit_pow == expected_unit


def test_unit_division_returns_expected_result(dimension):
    unit1 = Unit(1.0, dimension, ["a"])
    unit2 = Unit(2.0, dimension * dimension, ["b", "b"])

    # FIXME: Expected names
    expected_unit = Unit(0.5, dimension ** -1, ["a", "b⁻¹", "b⁻¹"])

    unit_div = unit1 / unit2

    assert unit_div == expected_unit


def test_unit_inverse_returns_expected_result(dimension):
    unit = Unit(2.0, dimension, ["a"])

    expected_unit = Unit(0.5, dimension ** -1, ["a⁻¹"])

    unit_div = 1 / unit

    assert unit_div == expected_unit


@pytest.mark.parametrize(
    "names,expected_str",
    [
        [["a"], "a"],
        [["bc"], "bc"],
        [["a", "a"], "a·a"],
        [["a²"], "a²"],
        [["a", "bc⁻¹"], "a·bc⁻¹"],
    ],
)
def test_unit_str_returns_expected_result(names, expected_str, dimension):
    unit = Unit(1.0, dimension, ["a"])
    expected_str = "a"

    assert str(unit) == expected_str
