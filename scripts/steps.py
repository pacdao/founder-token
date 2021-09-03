from brownie import *

from scripts.deploy import main as deploy


def main():
    c = deploy()
    steps = []
    max_range = 150
    for i in range(max_range):
        steps.append(c.minPrice())
        c.mint({"from": accounts[i % 10], "value": c.minPrice()})
    i = 0
    for s in steps:
        print(i, s / 10 ** 18)
        i += 1
    return steps
