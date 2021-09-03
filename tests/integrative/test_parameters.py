import pytest
from brownie.test import given, strategy


# @pytest.mark.skip(reason="Next Feature")
@given(amount=strategy("uint", max_value=100 * 10 ** 18))
def test_units_always_thousands(founder, amount, alice, step_price):
    val = founder.minPrice() + amount
    founder.mint({"from": alice, "value": val})
    wei_base = step_price
    assert founder.minPrice() / wei_base == founder.minPrice() // wei_base


# @pytest.mark.parametrize('amount', [0,1, 1000000000, 10 ** 15,10 ** 17,10 ** 18, 10 ** 18 -1, 10 ** 18 + 1, 5 * 10 ** 18 + 3737])
@given(amount=strategy("uint", max_value=5 * 10 ** 18))
def test_min_price_always_increases(founder, amount, alice, step_price):
    last_price = 0
    for i in range(5):
        val = founder.minPrice() + amount
        founder.mint({"from": alice, "value": val})
        assert val > last_price
        last_price = val
