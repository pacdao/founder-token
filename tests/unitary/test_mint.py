import brownie


def test_first_id_is_zero(founder):
    assert founder.currentId() == 0


def test_first_price_is_floor(founder, floor_price):
    assert founder.minPrice() == floor_price


def test_floor_price_updates_on_mint(founder_minted, floor_price, step_price):
    assert founder_minted.minPrice() == floor_price + step_price

def test_floor_price_updates_on_large_mint(founder, alice, floor_price, step_price):
    founder.mint({"from": alice, "value": floor_price + step_price * 10})
    assert founder.minPrice() == floor_price + step_price * 11



def test_id_updates_on_mint(founder_minted):
    assert founder_minted.currentId() == 1


def test_assert_token_received(founder_minted, alice):
    assert founder_minted.ownerOf(1) == alice


def test_cannot_mint_lower_amount(founder, alice, floor_price):
    with brownie.reverts():
        founder.mint({"from": alice, "value": floor_price - 1})


def test_cannot_mint_same_amount(founder, alice, floor_price):
    with brownie.reverts():
        founder.mint({"from": alice, "value": floor_price})

def test_token_uri(founder_minted):
    assert founder_minted.tokenURI(1) == "https://ipfs.io/ipfs/QmQ56uCWK8W2DzRnMpVyorSD1gvD2fepHtYgFqRVW4aMGm"
