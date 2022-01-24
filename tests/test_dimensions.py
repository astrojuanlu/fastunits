def test_dimensions_are_equal_to_themselves(dimension):
    assert dimension == dimension


def test_dimensions_product_is_equal_to_power(dimension):
    dim_prod = dimension * dimension
    dim_power = dimension ** 2

    assert dim_prod == dim_power
