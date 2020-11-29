// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.6.12;

import "@openzeppelinV3/contracts/math/SafeMath.sol";
import "../../interfaces/IUniswapV2SlidingOracle.sol";

contract MockSlidingOracle is IUniswapV2SlidingOracle {
    using SafeMath for uint256;

    function current(
        address tokenIn,
        uint256 amountIn,
        address tokenOut
    ) external view override returns (uint256) {
        require(tokenIn == address(0x1cEB5cB57C4D4E2b2433641b95Dd330A33185A44), "tokenIn needs to be KP3R");
        require(tokenOut == address(0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2), "tokenOut needs to be WETH");
        return amountIn;
    }
}
