import pytest
from brownie import config

@pytest.fixture
def andre(accounts):
    # Andre, giver of tokens, and maker of yield
    yield accounts[0]


@pytest.fixture
def token(andre, Token):
    yield andre.deploy(Token)


@pytest.fixture
def gov(accounts):
    # yearn multis... I mean YFI governance. I swear!
    yield accounts[1]


@pytest.fixture
def rewards(gov):
    yield gov  # TODO: Add rewards contract


@pytest.fixture
def guardian(accounts):
    # YFI Whale, probably
    yield accounts[2]


@pytest.fixture
def vault(pm, gov, rewards, guardian, token):
    Vault = pm(config["dependencies"][0]).Vault
    vault = guardian.deploy(Vault, token, gov, rewards, "", "")
    yield vault


@pytest.fixture
def strategist(accounts):
    # You! Our new Strategist!
    yield accounts[3]


@pytest.fixture
def keeper(accounts):
    # This is our trusty bot!
    yield accounts[4]


@pytest.fixture
def strategy(strategist, keeper, vault, Strategy):
    strategy = strategist.deploy(Strategy, vault)
    strategy.setKeeper(keeper)
    yield strategy


@pytest.fixture
def nocoiner(accounts):
    # Has no tokens (DeFi is a ponzi scheme!)
    yield accounts[5]


@pytest.fixture
def pleb(accounts, andre, token, vault):
    # Small fish in a big pond
    a = accounts[6]
    # Has 0.01% of tokens (heard about this new DeFi thing!)
    bal = token.totalSupply() // 10000
    token.transfer(a, bal, {"from": andre})
    # Unlimited Approvals
    token.approve(vault, 2 ** 256 - 1, {"from": a})
    # Deposit half their stack
    vault.deposit(bal // 2, {"from": a})
    yield a


@pytest.fixture
def chad(accounts, andre, token, vault):
    # Just here to have fun!
    a = accounts[7]
    # Has 0.1% of tokens (somehow makes money trying every new thing)
    bal = token.totalSupply() // 1000
    token.transfer(a, bal, {"from": andre})
    # Unlimited Approvals
    token.approve(vault, 2 ** 256 - 1, {"from": a})
    # Deposit half their stack
    vault.deposit(bal // 2, {"from": a})
    yield a


@pytest.fixture
def greyhat(accounts, andre, token, vault):
    # Chaotic evil, will eat you alive
    a = accounts[8]
    # Has 1% of tokens (earned them the *hard way*)
    bal = token.totalSupply() // 100
    token.transfer(a, bal, {"from": andre})
    # Unlimited Approvals
    token.approve(vault, 2 ** 256 - 1, {"from": a})
    # Deposit half their stack
    vault.deposit(bal // 2, {"from": a})
    yield a


@pytest.fixture
def whale(accounts, andre, token, vault):
    # Totally in it for the tech
    a = accounts[9]
    # Has 10% of tokens (was in the ICO)
    bal = token.totalSupply() // 10
    token.transfer(a, bal, {"from": andre})
    # Unlimited Approvals
    token.approve(vault, 2 ** 256 - 1, {"from": a})
    # Deposit half their stack
    vault.deposit(bal // 2, {"from": a})
    yield a
