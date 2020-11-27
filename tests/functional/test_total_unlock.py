import pytest
import brownie
from brownie import Wei


def test_empty(hegicKeep3r):
    assert hegicKeep3r.ethTotalUnlock([]) == 0


def test_simple(hegicKeep3r, mockHegicOptions):
    mockHegicOptions.addOption(Wei("1 ether"), Wei("0.1 ether"))
    mockHegicOptions.addOption(Wei("10 ether"), Wei("1 ether"))
    mockHegicOptions.addOption(Wei("100 ether"), Wei("10 ether"))

    assert hegicKeep3r.ethTotalUnlock(list(range(3))) == Wei("122.1 ether")


def test_with_non_expired(hegicKeep3r, mockHegicOptions):
    mockHegicOptions.addOption(Wei("1 ether"), Wei("0.1 ether"))
    mockHegicOptions.addNonExpiredOption()

    with brownie.reverts():
        hegicKeep3r.ethTotalUnlock(list(range(2)))
