import pytest
import brownie
from brownie import Wei


def test_with_different_quantities(hegicKeep3r):
    assert hegicKeep3r.weightedUnlockValue(0, Wei("1 ether")) == 0
    assert hegicKeep3r.weightedUnlockValue(34, Wei("10 ether")) == Wei("4.25 ether")
    assert hegicKeep3r.weightedUnlockValue(80, Wei("10 ether")) == Wei("10 ether")

    with brownie.reverts():
        hegicKeep3r.weightedUnlockValue(100, 1)
