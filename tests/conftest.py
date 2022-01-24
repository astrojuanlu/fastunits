from typing import TYPE_CHECKING

import numpy as np
import pytest

from fastunits.dimensions import Dimension

if TYPE_CHECKING:
    from npytypes.rational import rational as R
    from numpy.typing import NDArray


@pytest.fixture
def base():
    return "ABC"


@pytest.fixture
def dimension(base):
    vector = np.array([1, 0, 0])  # type: NDArray[R]

    return Dimension(vector, base)
