import pytest
import brownie
from brownie import Contract, chain, accounts, Wei


def test_wbtc(HegicKeep3r, deployer, alice, bob):
    kp3r = Contract.from_explorer("0x1ceb5cb57c4d4e2b2433641b95dd330a33185a44")
    hegicKeep3r = deployer.deploy(HegicKeep3r, kp3r)

    hegicOptions = Contract.from_explorer(hegicKeep3r.wbtcOptions())

    # Buy WBTC call @ 2k for tomorrow
    tx = hegicOptions.create(24 * 3600, 1, 2000, 2, {"from": bob, "value": bob.balance()})
    optionId = tx.events["Create"]["id"]

    assert hegicKeep3r.wbtcOptionUnlockable(optionId) == False

    # TimeTravel two days just to make sure
    chain.sleep(60 * 60 * 24 * 2)
    chain.mine(1)

    # Now option should be unlockable!
    assert hegicKeep3r.wbtcOptionUnlockable(optionId) == True

    # Only keepers can unlock through the keep3r contract
    with brownie.reverts():
        hegicKeep3r.wbtcUnlock(optionId, {"from": bob})

    # lot's of keep3r boiler plate
    keeper = accounts.at(kp3r.keeperList(0), force=True)
    helper = Contract.from_explorer(kp3r.KPRH())
    oracle = Contract.from_explorer(helper.UV2SO())
    oracleGov = accounts.at(oracle.governance(), force=True)
    oracle.setMinKeep(0, {"from": oracleGov})
    oracle.work({"from": keeper})

    # This should happen before
    kp3r.addJob(hegicKeep3r, {"from": oracleGov})
    kp3rWhale = accounts.at("0xf7aa325404f81cf34268657ddf2d046763a8c4ed", force=True)
    kp3r.approve(kp3r, 2 ** 256 - 1, {"from": kp3rWhale})
    kp3r.addCredit(kp3r, hegicKeep3r, Wei("1 ether"), {"from": kp3rWhale})

    t = hegicKeep3r.wbtcUnlock(optionId, {"from": keeper})
    assert t.events["Expire"]["id"] == optionId

    option = hegicOptions.options(optionId)
    assert option.dict()["state"] == 3
