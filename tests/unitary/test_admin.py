import brownie
from brownie_tokens import MintableForkToken


def test_mints_with_updated_metadata(founder, alice):
    new_data = "new_uri"
    founder.setDefaultMetadata(new_data, {"from": alice})
    founder.mint({"from": alice, "value": founder.minPrice()})
    assert founder.tokenURI(founder.totalSupply()) == founder.baseURI() + new_data


def test_new_owner_can_receive(founder_minted, alice, bob):
    founder_minted.updateBeneficiary(bob, {"from": alice})
    bob_init = bob.balance()
    founder_minted.withdraw({"from": alice})
    assert bob.balance() >= bob_init


def test_new_owner_can_withdraw(founder_minted, alice, bob):
    founder_minted.updateBeneficiary(bob, {"from": alice})
    bob_init = bob.balance()
    founder_minted.withdraw({"from": bob})
    assert bob.balance() > bob_init


def test_new_owner_can_update_metadata(founder, alice, bob):
    founder.updateBeneficiary(bob, {"from": alice})
    new_data = "new uri"
    founder.setDefaultMetadata(new_data, {"from": bob})
    founder.mint({"from": alice, "value": founder.minPrice()})
    assert founder.tokenURI(founder.totalSupply()) == founder.baseURI() + new_data


def test_nonowner_cannot_transfer(founder_minted, alice, bob):
    with brownie.reverts():
        founder_minted.updateBeneficiary(bob, {"from": bob})


def test_new_owner_can_update_owner(founder_minted, alice, bob):
    founder_minted.updateBeneficiary(bob, {"from": alice})
    founder_minted.updateBeneficiary(alice, {"from": bob})

    alice_init = alice.balance()
    founder_minted.withdraw({"from": bob})
    assert alice.balance() > alice_init


def test_fallback_receivable(founder, alice, bob):
    founder_init = founder.balance()
    bob.transfer(founder, 10 ** 18)
    assert founder.balance() - founder_init == 10 ** 18


def test_fallback_funds_withdrawable(founder, alice, bob):
    founder_init = founder.balance()
    bob.transfer(founder, 10 ** 18)
    alice_init = alice.balance()
    founder.withdraw({"from": alice})
    assert alice.balance() - alice_init == 10 ** 18 + founder_init


def test_set_token_uri(founder_minted, alice):
    init_uri = founder_minted.tokenURI(1)
    string = "test"
    founder_minted.setTokenUri(1, string, {"from": alice})
    assert founder_minted.tokenURI(1) == founder_minted.baseURI() + string


def test_non_admin_cannot_set_token_uri(founder_minted, bob):
    init_uri = founder_minted.tokenURI(1)
    string = "test"
    with brownie.reverts():
        founder_minted.setTokenUri(1, string, {"from": bob})
    assert founder_minted.tokenURI(1) == init_uri
