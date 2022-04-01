// SPDX-License-Identifier: MIT

pragma solidity >=0.7.0 <0.9;

import "@openzeppelin/contracts/access/Ownable.sol";

abstract contract Painter is Ownable{
  event Received(address indexed _from, uint256 _amount);
  uint256 public updateCost = 0;

  function paint(uint256 _number) external view virtual returns(string memory);
  
  function setUpdateCost(uint256 _cost) external onlyOwner{
    updateCost = _cost;
  }

  function getUpdateCost() external view returns(uint256){
    return updateCost;
  }

  receive() external payable virtual {
      emit Received(msg.sender, msg.value);
  }

  function withdraw() external virtual onlyOwner {

  // Do not remove this otherwise you will not be able to withdraw the funds.
  // =============================================================================
  (bool os, ) = payable(owner()).call{value: address(this).balance}("");
  require(os);
  // =============================================================================
  }

}
