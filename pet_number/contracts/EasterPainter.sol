// SPDX-License-Identifier: MIT

pragma solidity >=0.7.0 <0.9.0;

import "@openzeppelin/contracts/utils/Strings.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "./Painter.sol";

contract EasterPainter is Ownable, Painter {
  using Strings for uint256;
  

constructor() 
  
 {
    
  }
function background(uint256 number) internal pure virtual returns (string memory){
    uint256 colorB = (number)&0xFF;
    uint256 colorG = (number>>8)&0xFF;
    uint256 colorR = (number>>(8*2))&0xFF;
     return string(abi.encodePacked(
       '<g id="egg_layer_line" clip-path="url(#egg)" filter="url(#specfilter)">',
     '<rect width="500" height="500" fill="RGB(',
     colorR.toString(),',',
     colorG.toString(),',',
     colorB.toString(),')"/>'
     ));
  }

  function selectLayer(uint256 number, uint256 position) internal pure virtual returns (string memory){
    string[7] memory layers;
    uint8 decoration = uint8(number%7);
    uint256 colorB = (number>>8)&0xFF;
    uint256 colorG = (number>>(8*2))&0xFF;
    uint256 colorR = (number>>(8*3))&0xFF;
    uint256 colorB2 = (number>>8*4)&0xFF;
    uint256 colorG2 = (number>>(8*5))&0xFF;
    uint256 colorR2 = (number>>(8*6))&0xFF;
    string memory color = string(abi.encodePacked('"RGB(',
     colorR.toString(),',',
     colorG.toString(),',',
     colorB.toString(),')"'));
    string memory color2 = string(abi.encodePacked('"RGB(',
     colorR2.toString(),',',
     colorG2.toString(),',',
     colorB2.toString(),')"'));
     position = position*100;
    string memory strpos = position.toString();
    layers[0] = string(abi.encodePacked('<path transform="translate(0,',strpos,')" stroke=',color2,' stroke-width="60" id="north" d="m 0 0 h 500"/>'));
    layers[1] = string(abi.encodePacked('<path transform="translate(0,',strpos,')" stroke=',color,' stroke-width="10" id="north_z" fill="transparent" d="m 0 30 l 45, -60 l 45, 60 l 45, -60 l 45, 60 l 45, -60 l 45, 60 l 45, -60 l 45, 60 l 45, -60 l 45, 60 "/>'));
    layers[2] = string(abi.encodePacked('<path transform="translate(0,',strpos,')" stroke=',color,' stroke-width="10" id="north_s" fill="transparent" d="m 0 0 c 30 -70, 55 -70, 85 0 s 55 -70, 85 0s 55 -70, 85 0s 55 -70, 85 0s 55 -70, 85 0 s 55 -70, 85 0"/>'));
    layers[3] = string(abi.encodePacked('<g  transform="translate(0,',strpos,')" fill=',color,' ><circle cx="50" cy="20" r="10"/><circle cx="100" cy="-20" r="10"/><circle cx="140" cy="20" r="10"/>  <circle cx="180" cy="-20" r="10"/>  <circle cx="220" cy="20" r="10"/>  <circle cx="260" cy="-20" r="10"/>  <circle cx="300" cy="20" r="10"/>  <circle cx="340" cy="-20" r="10"/>  <circle cx="380" cy="20" r="10"/><circle cx="420" cy="-20" r="10"/></g>'));
    layers[4] = string(abi.encodePacked(
        layers[0],
        layers[1]
      ));
    layers[5] = string(abi.encodePacked(
        layers[0],
        layers[2]
      ));
    layers[6] = string(abi.encodePacked(
        layers[0],
        layers[3]
      ));
     return layers[decoration];
  }





  
  
  
  function clipPath()internal pure virtual returns(string memory){
      return string(abi.encodePacked(
        '<clipPath id="egg" transform="translate(250,250)">',
        '<path transform="scale(1.5, 1.5)" d="M 0 -125 c -42.601 0, -100 91.911, -100 151.51 s 49.218 100, 100 100 M 0 -125 c 42.601 0, 100 91.911, 100 151.51 s -49.218 100, -100 100 z"/>',
        '</clipPath>'
          ));
  }


  function egg(uint256 number) internal pure virtual returns (string memory){
      uint256 north = (number>>24)&0xFFFFFFFFFFFFFF;
      uint256 tropic = (number>>(56))&0xFFFFFFFFFFFFFF;
      uint256 equator = (number>>(56*2))&0xFFFFFFFFFFFFFF;
      uint256 south = (number>>(56*3))&0xFFFFFFFFFFFFFF;
     return string(abi.encodePacked(
      clipPath(),
      background(number),
      selectLayer(north,1),
      selectLayer(tropic,2),
      selectLayer(equator,3),
      selectLayer(south,4),
     '</g>'
     ));
  }

    function filters()internal pure virtual returns(string memory){
      return string(abi.encodePacked(
        '<filter id="shadowfilter">',
	      '<feGaussianBlur result="blurOut" in="SourceGraphic" stdDeviation="10" />',
        '</filter>',
        '<filter id = "specfilter">',
        '<feSpecularLighting result="specOut" specularExponent="20" lighting-color="#bbbbbb">',
        '<fePointLight x="250" y="0" z="150"/>',
        '</feSpecularLighting>',
        '<feComposite in="SourceGraphic" in2="specOut" operator="arithmetic" k1="0" k2="1" k3="1" k4="0"/>',
        '</filter>'
          ));
  }
      function shadow()internal pure virtual returns(string memory){
      return string(abi.encodePacked(
        '<g filter="url(#shadowfilter)" transform="translate(250,250)">',
        '<ellipse fill="hsla(0, 0%, 0%, 60%)" cx="0" cy="190" rx="150" ry="25" />',
        '<path transform="scale(1.5, 1.5)" d="M 0 -125" fill="transparent"/>',
        '</g>'
          ));
  }

    function paint(uint256 number)external pure override returns(string memory){
      
      // uint256 number = getPetNumber(_tokenId);
      uint256 bg1 = (number&65535)%361;
      uint256 bg2 = ((number>>16)&65535)%361;
      number = number>>32;
      
      return string(abi.encodePacked(
        '<svg xmlns="http://www.w3.org/2000/svg" width="500" height="500" >',
         '<defs><linearGradient id="nG" gradientTransform="rotate(45)"><stop offset="5%" stop-color="hsl(',bg1.toString(),',50%, 25%)"/>',
         '<stop offset="95%" stop-color="hsl(',bg2.toString(),',50%, 25%)"/></linearGradient></defs>',
        
        '<rect width="500" height="500" fill="url(\'#nG\')"/>',
        filters(),
        shadow(),
            egg(number),
        '</svg>'
          ));
  }

      
}