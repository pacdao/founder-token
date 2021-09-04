import brownie


def test_can_withdraw_as_alice(founder_minted, alice, bob):
    founder_minted.withdraw({"from": alice})
    init_balance = alice.balance()

    mint_price = founder_minted.minPrice() * 10
    founder_minted.mint({'from': bob, value: mint_price})
    founder_minted.withdraw({"from": alice})
    final_balance = alice.balance()
    assert final_balance - init_balance == mint_price


def test_can_withdraw_as_bob(founder_minted, alice, bob):
    founder_minted.withdraw({"from": alice})
    init_balance = alice.balance()

    mint_price = founder_minted.minPrice() * 10
    founder_minted.mint({'from': bob, value: mint_price})
    founder_minted.withdraw({"from": bob})
    final_balance = alice.balance()
    assert final_balance - init_balance == mint_price


def test_bob_gets_nothing_on_withdraw(founder_minted, bob):
    bob_balance = bob.balance()
    founder_minted.withdraw({"from": bob})
    assert bob.balance() <= bob_balance


def test_withdrawal_increases_balance(founder_minted, alice):
    init_balance = alice.balance()
    founder_minted.withdraw({"from": alice})
    final_balance = alice.balance()
    assert final_balance > init_balance


def test_can_receive_funds_through_fallback(founder, alice, bob):
    init_balance = alice.balance()
    bob_balance = bob.balance()
    bob.transfer(founder, bob_balance)
    founder.withdraw({"from": alice})
    final_balance = alice.balance()
    assert final_balance - init_balance >= bob_balance
