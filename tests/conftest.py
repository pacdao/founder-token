#!/usr/bin/python3

import pytest
from brownie import PACFounder, Wei


@pytest.fixture(scope="function", autouse=True)
def isolate(fn_isolation):
    # perform a chain rewind after completing each test, to ensure proper isolation
    # https://eth-brownie.readthedocs.io/en/v1.10.3/tests-pytest-intro.html#isolation-fixtures
    pass


@pytest.fixture(scope="module")
def alice(accounts):
    return accounts[0]


@pytest.fixture(scope="module")
def bob(accounts):
    return accounts[1]


@pytest.fixture(scope="module")
def floor_price():
    return Wei(".0001 ether")


@pytest.fixture(scope="module")
def step_price():
    return Wei(".0001 ether")


@pytest.fixture(scope="module")
def founder(alice, floor_price, step_price):
    return PACFounder.deploy(alice, {"from": alice})


@pytest.fixture(scope="function")
def founder_minted(accounts, founder, floor_price):
    for i in range(10):
        founder.mint({"from": accounts[i], "value": founder.minPrice()})
    return founder
