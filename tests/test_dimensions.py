from typing import TYPE_CHECKING

import numpy as np
import pytest

from fastunits.dimensions import Dimension

if TYPE_CHECKING:
    from npytypes.rational import rational as R
    from numpy.typing import NDArray


@pytest.fixture
def dimension():
    base = "ABC"
    vector = np.array([1, 0, 0])  # type: NDArray[R]

    return Dimension(vector, base)


def test_dimensions_are_equal_to_themselves(dimension):
    assert dimension == dimension


def test_dimensions_product_is_equal_to_power(dimension):
    dim_prod = dimension * dimension
    dim_power = dimension ** 2

    assert dim_prod == dim_power
