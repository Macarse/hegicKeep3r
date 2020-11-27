import pytest
import brownie


def test_initial_values(deployer, hegicKeep3r):
    hegicKeep3r.name() == "Hegic Keep3r"
    hegicKeep3r.governor() == deployer
    hegicKeep3r.unlockGasCost() == 175_000


def test_set_unlock_gas(hegicKeep3r):
    tx = hegicKeep3r.setUnlockGasCost(888_000)
    assert tx.events["UnlockGasCostSet"]["unlockGasCost"] == 888_000
    assert hegicKeep3r.unlockGasCost() == 888_000
