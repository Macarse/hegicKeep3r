import pytest


@pytest.fixture
def mockedHegicOptions(deployer, MockedHegicOptions):
    yield deployer.deploy(MockedHegicOptions)


@pytest.fixture
def hegicKeep3r(deployer, HegicKeep3r, mockedHegicOptions):
    kp3r = "0x1ceb5cb57c4d4e2b2433641b95dd330a33185a44"
    yield deployer.deploy(
        HegicKeep3r, kp3r, kp3r, kp3r, mockedHegicOptions, mockedHegicOptions
    )
