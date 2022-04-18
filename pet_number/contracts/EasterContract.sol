// SPDX-License-Identifier: MIT

pragma solidity >=0.7.0 <0.9.0;

import "@openzeppelin/contracts/access/Ownable.sol";
interface PetNumber{
    function balanceOf(
    address owner
  )
    external
    view
    returns (
      uint256 balance
    );
    function tokenOfOwnerByIndex(address owner, uint256 index) external view returns (uint256 tokenId);
    function getPetTraits(uint256 _tokenId) external view returns(uint8 zeros, uint8 ones, uint8 twos, uint8 threes);
}

contract EasterContract is Ownable {

 
    // address constant public petContract=0xCFf08957F6eF129022ddE6569B57002f31AE8c91;
    event Received(address indexed _from, uint256 _amount);
    event Rewarded(address indexed _to, uint256 _amount);
    PetNumber public pet; 
    uint256 public lastTokenId=0;
    mapping(uint256 => bool) rewardedNFTs;
    constructor(address _petAddress){
        pet = PetNumber(payable(_petAddress));
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

    function setLastTokenId(uint256 _lastTokenId) external onlyOwner {
        lastTokenId = _lastTokenId;
    }

    function potentialReward() external view returns(bool) {
        uint256 thisBalance = address(this).balance;
        if (thisBalance<=0) return false;
        for (uint256 i=0; i<pet.balanceOf(msg.sender);i++){
            uint256 ownerTokenId = pet.tokenOfOwnerByIndex(msg.sender, i);
            if (ownerTokenId>lastTokenId && !rewardedNFTs[ownerTokenId]){
                uint256 zeros=0;
                uint256 ones=0;
                uint256 twos=0;
                uint256 threes=0;
                (zeros, ones, twos, threes) = pet.getPetTraits(ownerTokenId);
                if (zeros>0){

                    return true;
                }
            }
        }
        return false;
        
    }

    function getReward() external returns(bool){
        uint256 thisBalance = address(this).balance;
        require(thisBalance>0,"Balance is 0");
        for (uint256 i=0; i<pet.balanceOf(msg.sender);i++){
            uint256 ownerTokenId = pet.tokenOfOwnerByIndex(msg.sender, i);
            if (ownerTokenId>lastTokenId && !rewardedNFTs[ownerTokenId]){
                uint256 zeros=0;
                uint256 ones=0;
                uint256 twos=0;
                uint256 threes=0;
                (zeros, ones, twos, threes) = pet.getPetTraits(ownerTokenId);
                if (zeros>0){

                    uint256 extractValue = thisBalance < 5 ether ? thisBalance : 5 ether;
                    (bool os, ) = payable(msg.sender).call{value: extractValue}("");
                    require(os);
                    rewardedNFTs[ownerTokenId] = true;
                    emit Rewarded(msg.sender, extractValue);
                    return true;
                }
            }
        }
        return false;
        
    }

}