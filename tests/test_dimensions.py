import numpy as np
import pytest
from npytypes.rational import rational as R

from fastunits.dimensions import Dimension, dimensions_from_base


def test_dimensions_are_equal_to_themselves(dimension):
    assert dimension == dimension


def test_dimensions_product_is_equal_to_power(dimension):
    dim_prod = dimension * dimension
    dim_power = dimension ** 2

    assert dim_prod == dim_power


def test_dimension_create_returns_expected_result():
    base = "ABC"
    expected_dimension = Dimension(np.array([1, 0, 0], dtype=R), base=base)

    dimension = Dimension.create("A", "ABC")

    assert dimension == expected_dimension


def test_dimensions_from_base_returns_expected_dimensions():
    base = "ABC"
    expected_A = Dimension(np.array([1, 0, 0], dtype=R), base=base)
    expected_B = Dimension(np.array([0, 1, 0], dtype=R), base=base)
    expected_C = Dimension(np.array([0, 0, 1], dtype=R), base=base)

    A, B, C = dimensions_from_base(base)

    assert A == expected_A
    assert B == expected_B
    assert C == expected_C


@pytest.mark.parametrize(
    "vector,expected_str",
    [
        [np.array([1, 0, 0], dtype=R), "A¹B⁰C⁰"],
        [np.array([0, 1, 0], dtype=R), "A⁰B¹C⁰"],
        [np.array([0, 0, 1], dtype=R), "A⁰B⁰C¹"],
        [np.array([0, 0, 0], dtype=R), "A⁰B⁰C⁰"],
        [np.array([1, 1, 1], dtype=R), "A¹B¹C¹"],
        [np.array([R(1, 2), 0, 0], dtype=R), "A¹⸍²B⁰C⁰"],
        [np.array([R(-1, 2), 0, 0], dtype=R), "A⁻¹⸍²B⁰C⁰"],
    ],
)
def test_dimensions_str_returns_expected_result(vector, expected_str):
    base = "ABC"
    dimension = Dimension(vector, base=base)

    assert str(dimension) == expected_str
