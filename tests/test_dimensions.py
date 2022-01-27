import numpy as np
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
