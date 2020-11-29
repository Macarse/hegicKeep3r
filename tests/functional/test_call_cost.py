import pytest
import brownie
from brownie import Wei


def test_with_different_quantities(hegicKeep3r):
    with brownie.reverts():
        hegicKeep3r.ethCallCost(0)

    # 175_000 * n * gasPrice * 1.1
    # We don't take account kp3r to eth since mock oracle is 1:1
    assert hegicKeep3r.ethCallCost(1) == Wei("0.003465 ether")
    assert hegicKeep3r.ethCallCost(2) == Wei("0.006930 ether")
    assert hegicKeep3r.ethCallCost(10) == Wei("0.03465 ether")
