// SPDX-License-Identifier: MIT
pragma solidity >=0.6.12;
pragma experimental ABIEncoderV2;

import "../../interfaces/hegic/IHegic.sol";

// Mock for
//ethPool = address(0x878F15ffC8b894A1BA7647c7176E4C01f74e140b);
//wbtcPool = address(0x20dd9e22d22dd0a6ef74a520cb08303b5fad5de7);

contract MockedHegicPool is IHegicPool {

    uint256 public mockedTotalBalance;
    uint256 public mockedAvailableBalance;

    constructor() public {
    }

    function setMockedTotalBalance(uint256 _mockedTotalBalance) external {
        mockedTotalBalance = _mockedTotalBalance;
    }

    function totalBalance() external override view returns (uint256 amount) {
        return mockedTotalBalance;
    }

    function setMockedAvailableBalance(uint256 _mockedAvailableBalance) external {
        mockedAvailableBalance = _mockedAvailableBalance;
    }

    function availableBalance() external override view returns (uint256 amount) {
        return mockedAvailableBalance;
    }
}
