from brownie import *


def test_first_ten_floor_mints_under_gas(founder):
    for i in range(10):
        assert founder.minPrice() < Wei(".015 ether")
        founder.mint({"from": accounts[i], "value": founder.minPrice()})


def test_first_fifty_mints_under_1kusd(founder):
    for i in range(50):
        assert founder.minPrice() < Wei(".2 ether")
        founder.mint({"from": accounts[i // 5], "value": founder.minPrice()})


def test_mint_100_between_dot1_to_1_eth(founder):
    for i in range(100):
        founder.mint({"from": accounts[i // 10], "value": founder.minPrice()})
    assert founder.minPrice() > 10 ** 17
    assert founder.minPrice() < 10 ** 18


def test_deploy_price_reasonable(founder):
    assert history[-1].gas_used * Wei("50 gwei") / 10 ** 18 < 0.11155015


def test_non_beneficiary_can_deploy(alice, bob, floor_price, step_price):
    PACFounder.deploy(bob, {"from": alice})
