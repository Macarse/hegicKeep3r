// SPDX-License-Identifier: MIT
pragma solidity >=0.6.12;
pragma experimental ABIEncoderV2;

import "@openzeppelinV3/contracts/math/SafeMath.sol";

import "../../interfaces/hegic/IHegic.sol";
import "../../interfaces/Keep3r/IHegicKeep3r.sol";
import "../../interfaces/IKeep3rV1Helper.sol";
import "../../interfaces/IUniswapV2SlidingOracle.sol";
import "../utils/Governable.sol";
import "../utils/CollectableDust.sol";

import "./Keep3rAbstract.sol";

contract HegicKeep3r is Governable, CollectableDust, Keep3r, IHegicKeep3r {
    using SafeMath for uint256;

    address public keep3rHelper;
    address public slidingOracle;
    address public ethOptions;
    address public wbtcOptions;
    uint256 public unlockGasCost;

    address public constant KP3R = address(0x1cEB5cB57C4D4E2b2433641b95Dd330A33185A44);
    address public constant WETH = address(0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2);

    constructor(
        address _keep3r,
        address _keep3rHelper,
        address _slidingOracle,
        address _ethOptions,
        address _wbtcOptions,
        uint256 _unlockGasCost
    ) public Governable(msg.sender) CollectableDust() Keep3r(_keep3r) {
        keep3rHelper = _keep3rHelper;
        slidingOracle = _slidingOracle;
        ethOptions = _ethOptions;
        wbtcOptions = _wbtcOptions;
        unlockGasCost = _unlockGasCost;
    }

    // Getters
    function name() external pure override returns (string memory) {
        return "Hegic Keep3r";
    }

    function ethOptionUnlockable(uint256 _optionId) external override view returns (bool) {
        // Option memory option = IHegic(ethOptions).options(_optionId);
        // return option.state == State.Active && option.expiration < block.timestamp;
        return false;
    }

    function wbtcOptionUnlockable(uint256 _optionId) external override view returns (bool) {
        // Option memory option = IHegic(wbtcOptions).options(_optionId);
        // return option.state == State.Active && option.expiration < block.timestamp;
        return false;
    }

    // Keep3r actions
    function ethUnlock(uint256 _optionId) external override paysKeeper {
        //IHegic(ethOptions).unlock(_optionId);
    }

    function wbtcUnlock(uint256 _optionId) external override paysKeeper {
        //IHegic(wbtcOptions).unlock(_optionId);
    }

    // Helpers
    function ethCallCost(uint256 optionsQty) external override view returns (uint256) {
        require(optionsQty > 0);

        uint256 kp3rCallCost = IKeep3rV1Helper(keep3rHelper).getQuoteLimit(optionsQty.mul(unlockGasCost));
        return IUniswapV2SlidingOracle(slidingOracle).current(KP3R, kp3rCallCost, WETH);
    }

    function ethPoolUsage() external override view returns (uint256) {
        return _poolUsage(ethOptions);
    }

    function wbtcPoolUsage() external override view returns (uint256) {
        return _poolUsage(wbtcOptions);
    }

    function _poolUsage(address hegic) internal view returns (uint256) {
        address pool = IHegicOptions(ethOptions).pool();
        uint256 availableBalance = IHegicPool(pool).availableBalance();
        uint256 totalBalance = IHegicPool(pool).totalBalance();

        // Shouldn't happen
        if (totalBalance == 0) {
            return 0;
        }

        return uint256(100).sub(availableBalance.mul(100).div(totalBalance));
    }

    function ethTotalUnlock(uint256[] calldata optionIDs) external override view returns (uint256) {
        return _totalUnlock(ethOptions, optionIDs);
    }

    function wbtcTotalUnlock(uint256[] calldata optionIDs) external override view returns (uint256) {
        return _totalUnlock(wbtcOptions, optionIDs);
    }

    function _totalUnlock(address hegic, uint256[] calldata optionIDs) internal view returns (uint256) {
        uint256 len = optionIDs.length;
        uint256 totalUnlock = 0;

        for (uint256 i = 0; i < len; i++) {
            Option memory option = IHegicOptions(hegic).options(optionIDs[i]);
            require(option.state == State.Active && option.expiration < block.timestamp);

            totalUnlock += option.lockedAmount;
            totalUnlock += option.premium;
        }

        return totalUnlock;
    }

    // Governable
    function setPendingGovernor(address _pendingGovernor) external override onlyGovernor {
        _setPendingGovernor(_pendingGovernor);
    }

    function acceptGovernor() external override onlyPendingGovernor {
        _acceptGovernor();
    }

    function setUnlockGasCost(uint256 _unlockGasCost) external override onlyGovernor {
        unlockGasCost = _unlockGasCost;
        emit UnlockGasCostSet(_unlockGasCost);
    }

    function setKeep3r(address _keep3r) external override onlyGovernor {
        _setKeep3r(_keep3r);
        emit Keep3rSet(_keep3r);
    }

    function setKeep3rHelper(address _keep3rHelper) external override onlyGovernor {
        keep3rHelper = _keep3rHelper;
        emit Keep3rHelperSet(_keep3rHelper);
    }

    function setSlidingOracle(address _slidingOracle) external override onlyGovernor {
        slidingOracle = _slidingOracle;
        emit SlidingOracleSet(_slidingOracle);
    }

    // Collectable Dust
    function sendDust(
        address _to,
        address _token,
        uint256 _amount
    ) external override onlyGovernor {
        _sendDust(_to, _token, _amount);
    }
}
