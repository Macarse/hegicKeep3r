import pytest
from brownie import Wei


@pytest.fixture
def oracle(deployer, MockSlidingOracle):
    yield deployer.deploy(MockSlidingOracle)


@pytest.fixture
def mockKeep3rHelper(deployer, MockKeep3rHelper):
    yield deployer.deploy(MockKeep3rHelper)


@pytest.fixture
def mockHegicPool(deployer, MockHegicPool):
    yield deployer.deploy(MockHegicPool)


@pytest.fixture
def mockHegicOptions(deployer, MockHegicOptions, mockHegicPool):
    yield deployer.deploy(MockHegicOptions, mockHegicPool)


@pytest.fixture
def hegicKeep3r(deployer, HegicKeep3r, mockHegicOptions, mockKeep3rHelper, oracle):
    kp3r = "0x1ceb5cb57c4d4e2b2433641b95dd330a33185a44"
    unlockGasCost = 175_000
    yield deployer.deploy(
        HegicKeep3r,
        kp3r,
        mockKeep3rHelper,
        oracle,
        mockHegicOptions,
        mockHegicOptions,
        unlockGasCost,
    )
