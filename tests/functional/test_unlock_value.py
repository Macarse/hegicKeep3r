import pytest
import brownie
from brownie import Wei


def test_with_different_quantities(hegicKeep3r):
    assert hegicKeep3r.unlockValue(Wei("1 ether")) == Wei("0.1 ether")
    assert hegicKeep3r.unlockValue(Wei("0 ether")) == Wei("0 ether")
    assert hegicKeep3r.unlockValue(Wei("10 ether")) == Wei("1 ether")
