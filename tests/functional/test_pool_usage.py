import pytest
import brownie
from brownie import Wei


def test_empty(hegicKeep3r, mockHegicPool):
    mockHegicPool.setMockedTotalBalance(0)
    mockHegicPool.setMockedAvailableBalance(0)
    assert hegicKeep3r.ethPoolUsage() == 0


def test_max_usage(hegicKeep3r, mockHegicPool):
    mockHegicPool.setMockedTotalBalance(10)
    mockHegicPool.setMockedAvailableBalance(0)
    assert hegicKeep3r.ethPoolUsage() == 100


def test_zero_usage(hegicKeep3r, mockHegicPool):
    mockHegicPool.setMockedTotalBalance(100)
    mockHegicPool.setMockedAvailableBalance(100)
    assert hegicKeep3r.ethPoolUsage() == 0


def test_typical_usage(hegicKeep3r, mockHegicPool):
    mockHegicPool.setMockedTotalBalance(61279512544644677148795)
    mockHegicPool.setMockedAvailableBalance(40817085544644677148795)

    # 100-(pool.availableBalance() * 100 / pool.totalBalance())
    assert hegicKeep3r.ethPoolUsage() == 34
