// SPDX-License-Identifier: MIT
pragma solidity >=0.6.12;
pragma experimental ABIEncoderV2;

import "../../interfaces/hegic/IHegic.sol";

// Mock for
//ethOptions = address(0xEfC0eEAdC1132A12c9487d800112693bf49EcfA2);
//wbtcOptions = address(0x3961245DB602eD7c03eECcda33eA3846bD8723BD);

contract MockedHegicOptions is IHegic {

    Option[] public mockedOptions;

    // Mock helpers
    function addOption(uint256 lockedAmount, uint256 premium) external {
      Option memory option = Option(
          State.Active, // state
          msg.sender, // holder
          100, // strike
          1, //amount
          lockedAmount, // lockedAmount
          premium, // premium
          1606406162, // expiration
          OptionType.Call // optionType
      );

      mockedOptions.push(option);
    }

    function addNonExpiredOption() external {
      Option memory option = Option(
          State.Active, // state
          msg.sender, // holder
          100, // strike
          1, //amount
          1, // lockedAmount
          1, // premium
          block.timestamp + 10000, // expiration
          OptionType.Call // optionType
      );

      mockedOptions.push(option);
    }

    function unlockAll(uint256[] calldata optionsIDs) external override {

    }

    function options(uint256 optionId) external override view returns (Option memory) {
        return mockedOptions[optionId];
    }
}
