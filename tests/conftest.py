import pytest
from brownie import config


@pytest.fixture
def deployer(accounts):
    yield accounts[0]


@pytest.fixture
def bob(accounts):
    yield accounts[1]


@pytest.fixture
def alice(accounts):
    yield accounts[2]
