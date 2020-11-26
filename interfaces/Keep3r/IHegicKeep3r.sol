// SPDX-License-Identifier: MIT
pragma solidity >=0.6.12;

interface IHegicKeep3r {
    event Keep3rSet(address keep3r);
    event Keep3rHelperSet(address keep3rHelper);
    event SlidingOracleSet(address slidingOracle);

    // Actions by Keeper
    event EthOptionUnlockedByKeeper(uint256 _optionId);
    event WbtcOptionUnlockedByKeeper(uint256 _optionId);

    // Setters
    function setKeep3r(address _keep3r) external;
    function setKeep3rHelper(address _keep3rHelper) external;
    function setSlidingOracle(address _slidingOracle) external;

    // Getters
    function ethOptionUnlockable(uint256 _optionId) external view returns (bool);
    function wbtcOptionUnlockable(uint256 _optionId) external view returns (bool);

    // Keep3r actions
    function ethUnlock(uint256 _optionId) external;
    function wbtcUnlock(uint256 _optionId) external;

    // Helpers
    function ethCalculateTotalUnlock(uint256[] calldata optionIDs) external view returns (uint256);

    // Name of the Keep3r
    function name() external pure returns (string memory);

}
