// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.6.8;

import "@openzeppelinV3/contracts/math/SafeMath.sol";
import "../../interfaces/IKeep3rV1Helper.sol";

contract MockKeep3rHelper is IKeep3rV1Helper {
    using SafeMath for uint256;

    uint256 constant gasCost = 18000000000;

    constructor() public {}

    function getQuoteLimit(uint256 gasUsed) external view override returns (uint256) {
        return gasUsed.mul(gasCost).mul(11).div(10);
    }
}
