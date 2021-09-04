import brownie
from brownie import Wei, history


def test_airdrop_reserves_10(founder_minted):
    assert founder_minted.currentId() == 20


def test_deployer_received_10(founder, alice, bob):
    for i in range(20):
        founder.mint({'from': bob, 'value': founder.minPrice()})
    tally = 0
    for i in range(founder.totalSupply()):
        if founder.ownerOf(i + 1) == alice:
            tally += 1
    assert tally == 10


def test_first_price_is_floor(founder, floor_price):
    assert founder.minPrice() == floor_price


def test_floor_price_updates_on_mint(founder_minted, step_price, alice):
    floor_price = founder_minted.minPrice()
    founder_minted.mint({'from': alice, 'value': floor_price})

    assert founder_minted.minPrice() == floor_price + step_price


def test_floor_price_updates_on_large_mint(founder_minted, alice, floor_price, step_price):
    founder = founder_minted
    founder.mint({"from": alice, "value": floor_price + step_price * 10})
    assert founder.minPrice() == floor_price + step_price * 11


def test_id_updates_on_mint(founder_minted, bob):
    founder = founder_minted
    first_id = founder.currentId()
    founder.mint({'from': bob, 'value': founder.minPrice()})
    assert founder.currentId() == first_id + 1


def test_assert_token_received(founder_minted, bob):
    founder = founder_minted
    founder.mint({'from': bob, 'value': founder.minPrice()})
    assert founder.ownerOf(founder.currentId()) == bob


def test_cannot_mint_lower_amount(founder, alice, floor_price):
    with brownie.reverts():
        founder.mint({"from": alice, "value": floor_price - 1})


def test_cannot_mint_same_amount(founder_minted, alice, bob):
    floor_price = founder_minted.minPrice()
    founder_minted.mint({'from': bob, 'value': floor_price})

    with brownie.reverts():
        founder_minted.mint({"from": alice, "value": floor_price})


def test_token_uri_ipfs(founder_minted):
    assert founder_minted.tokenURI(1)[0:7] == "ipfs://"


def test_mint_price_reasonable(founder, alice):
    founder.mint({'from': alice, 'value': founder.minPrice()})
    assert history[-1].gas_used * Wei("50 gwei") / 10 ** 18 < 0.02
