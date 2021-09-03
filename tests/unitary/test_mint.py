import brownie
from brownie import Wei, history


def test_airdrop_reserves_10(founder):
    assert founder.currentId() == 10


def test_deployer_received_10(founder, alice):
    for i in range(10):
        assert founder.ownerOf(1+i) == alice


def test_first_price_is_floor(founder, floor_price):
    assert founder.minPrice() == floor_price


def test_floor_price_updates_on_mint(founder_minted, floor_price, step_price):
    assert founder_minted.minPrice() == floor_price + step_price


def test_floor_price_updates_on_large_mint(founder, alice, floor_price, step_price):
    founder.mint({"from": alice, "value": floor_price + step_price * 10})
    assert founder.minPrice() == floor_price + step_price * 11


def test_id_updates_on_mint(founder, bob):
    first_id = founder.currentId()
    founder.mint({'from': bob, 'value': founder.minPrice()})
    assert founder.currentId() == first_id + 1


def test_assert_token_received(founder, bob):
    founder.mint({'from': bob, 'value': founder.minPrice()})
    assert founder.ownerOf(founder.currentId()) == bob


def test_cannot_mint_lower_amount(founder, alice, floor_price):
    with brownie.reverts():
        founder.mint({"from": alice, "value": floor_price - 1})


def test_cannot_mint_same_amount(founder, alice, floor_price):
    with brownie.reverts():
        founder.mint({"from": alice, "value": floor_price})


def test_token_uri_ipfs(founder_minted):
    assert founder_minted.tokenURI(1)[0:7] == "ipfs://"


def test_mint_price_reasonable(founder_minted):
    assert history[-1].gas_used * Wei("50 gwei") / 10 ** 18 < 0.02
