// SPDX-License-Identifier: MIT
pragma solidity >=0.6.12;
pragma experimental ABIEncoderV2;

enum State {Inactive, Active, Exercised, Expired}
enum OptionType {Invalid, Put, Call}

struct Option {
    State state;
    address payable holder;
    uint256 strike;
    uint256 amount;
    uint256 lockedAmount;
    uint256 premium;
    uint256 expiration;
    OptionType optionType;
}

interface IHegic {

    function unlockAll(uint256[] calldata optionsIDs) external;

    function options(uint256) external view returns (Option memory);

}
