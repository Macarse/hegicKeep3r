import pytest
import brownie
from brownie import Contract, chain, accounts, Wei


@pytest.mark.require_network("mainnet-fork")
def test_wbtc(HegicKeep3r, deployer, alice, bob):
    kp3r = Contract.from_explorer("0x1ceb5cb57c4d4e2b2433641b95dd330a33185a44")
    unlockGasCost = 175_000
    unlockValueMultiplier = 10
    ethOptions = "0xEfC0eEAdC1132A12c9487d800112693bf49EcfA2"
    wbtcOptions = "0x3961245DB602eD7c03eECcda33eA3846bD8723BD"
    helper = "0x93747c4260E64507A213B4016e1d435C9928617f"
    oracle = "0x73353801921417F465377c8d898c6f4C0270282C"

    hegicKeep3r = deployer.deploy(
        HegicKeep3r,
        kp3r,
        helper,
        oracle,
        ethOptions,
        wbtcOptions,
        unlockGasCost,
        unlockValueMultiplier,
    )
    hegicOptions = Contract.from_explorer(hegicKeep3r.wbtcOptions())
    optionIDs = [0, 0, 0]

    # Buy 3 different ETH call @ 2k for tomorrow
    tx = hegicOptions.create(
        24 * 3600, 1e8, 200_000 * 1e8, 2, {"from": bob, "value": bob.balance()}
    )
    optionIDs[0] = tx.events["Create"]["id"]

    tx = hegicOptions.create(
        24 * 3600, 2 * 1e8, 200_000 * 1e8, 2, {"from": bob, "value": bob.balance()}
    )
    optionIDs[1] = tx.events["Create"]["id"]
    tx = hegicOptions.create(
        24 * 3600, 10 * 1e8, 200_000 * 1e8, 2, {"from": bob, "value": bob.balance()}
    )
    optionIDs[2] = tx.events["Create"]["id"]

    assert hegicKeep3r.wbtcOptionsUnlockable(optionIDs) == False

    # TimeTravel two days just to make sure
    chain.sleep(60 * 60 * 24 * 2)
    chain.mine(1)

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

    # Now option should be unlockable!
    assert hegicKeep3r.wbtcOptionsUnlockable(optionIDs) == True

    # Only keepers can unlock through the keep3r contract
    with brownie.reverts():
        hegicKeep3r.wbtcUnlockAll(optionIDs, {"from": bob})

    t = hegicKeep3r.wbtcUnlockAll(optionIDs, {"from": keeper})
    assert t.events["Expire"][0]["id"] == optionIDs[0]
    assert t.events["Expire"][1]["id"] == optionIDs[1]
    assert t.events["Expire"][2]["id"] == optionIDs[2]

    for i in range(3):
        option = hegicOptions.options(optionIDs[i])
        assert option.dict()["state"] == 3
