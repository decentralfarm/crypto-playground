// SPDX-License-Identifier: MIT

pragma solidity >=0.7.0 <0.9.0;

import "@openzeppelin/contracts/utils/Strings.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "./Painter.sol";

contract SwordPainter is Ownable, Painter {
  using Strings for uint256;
  

constructor() 
  
 {
    
  }

  function blade(uint256 number) internal pure virtual returns (string memory){
    string[2] memory shapes =[
    '"M 250 10 L 225 110 C 235 110, 235 370, 225 370 H 275 C 265 370, 265 110, 275 110 Z V 350 L 225 370 H 275 L 250 350"',
    '"M 250 10 L 225 110 v 260 H 275 V 110 Z V 350 L 225 370 H 275 L 250 350"'
    ];
    uint8 shape = uint8(number&1);
    uint256 colorB = (number>>8)&0xFF;
    uint256 colorG = (number>>(8*2))&0xFF;
    uint256 colorR = (number>>(8*3))&0xFF;
     return string(abi.encodePacked(
     '<path stroke="black" d=',
     shapes[shape],
     ' fill="RGB(',
     colorR.toString(),',',
     colorG.toString(),',',
     colorB.toString(),')"/>'
     ));
  }

function crossguard(uint256 number) internal pure virtual returns (string memory){
     uint8 shape = uint8(number&0xFF);
    uint256 colorB = (number>>8)&0xFF;
    uint256 colorG = (number>>(8*2))&0xFF;
    uint256 colorR = (number>>(8*3))&0xFF;
     return string(abi.encodePacked(
     '<path stroke="black" d="M 215 370 C 215 400, 285 400, 285 370 Z" fill="RGB(',
     colorR.toString(),',',
     colorG.toString(),',',
     colorB.toString(),')"/>'
     ));
  }

  function grip(uint256 number) internal pure virtual returns (string memory){
    string[3] memory shapes;
    uint8 shape = uint8(number&0xFF);
    uint256 colorB = (number>>8)&0xFF;
    uint256 colorG = (number>>(8*2))&0xFF;
    uint256 colorR = (number>>(8*3))&0xFF;
    string memory gripColor = string(abi.encodePacked(
      'stroke="black" fill="RGB(',
     colorR.toString(),',',
     colorG.toString(),',',
     colorB.toString(),')"/>'
     ));
    shapes[0]=string(abi.encodePacked(
      '<path d="M 238 392 C 238 393, 262 393, 262 392 V 456 C 262 454, 238 454, 238 456 V 392 " ',
      gripColor
      ));
    shapes[1]=string(abi.encodePacked(
      shapes[0],
      '<ellipse cx="250" cy="400" rx="15" ry="5" ',gripColor,
      '<ellipse cx="250" cy="420" rx="15" ry="5" ',gripColor,
      '<ellipse cx="250" cy="440" rx="15" ry="5" ',gripColor
      ));
    shapes[2] = string(abi.encodePacked(
      '<path d="M 238 392 C 238 393, 262 393, 262 392 Q 256 399, 262 406 v 3 Q 256 416, 262 423 v 3 Q 256 433, 262 440 v 3 Q 256 450, 262 456 C 262 454, 238 454, 238 456 Q 244 450, 238 443 v -3 Q 244 433, 238 426 v -3 Q 244 416, 238 409 v -3 Q 244 399, 238 392 M 238 406 h 24 M 238 409 h 24 M 238 423 h 24 M 238 426 h 24 M 238 440 h 24 M 238 443 h 24" ',
      gripColor
    ));

     return shapes[shape%3];
  }

  
  function pommel(uint256 number) internal pure virtual returns (string memory){
    string[6] memory shapes;
    uint8 shape = uint8(number&0xFF);
    uint256 color1B = (number>>8)&0xFF;
    uint256 color1G = (number>>(8*2))&0xFF;
    uint256 color1R = (number>>(8*3))&0xFF;
    uint256 color2B = (number>>(8*4))&0xFF;
    uint256 color2G = (number>>(8*5))&0xFF;
    uint256 color2R = (number>>(8*6))&0xFF;
    string memory gemColor = string(abi.encodePacked(
      'stroke="black" fill="RGB(',
     color2R.toString(),',',
     color2G.toString(),',',
     color2B.toString(),')"/>'
      
     ));
     shapes[0] = string(abi.encodePacked(
       '<circle cx="250" cy="475" r="12" ',
        gemColor
       ));
     shapes[1] = string(abi.encodePacked(
        '<polygon points="250,463 262,475 250,487 238,475" ',
        gemColor
        ));
     shapes[2] =  string(abi.encodePacked(
        '<polygon points="250,463 239.61,469 239.61,481 250,487 260.39,481 260.39,469" ',
        gemColor
        ));
      shapes[3] = string(abi.encodePacked(
        shapes[0],
        shapes[1]
      ));

      shapes[4] = string(abi.encodePacked(
        shapes[0],
        shapes[2]
      ));
      shapes[5] = string(abi.encodePacked(
        shapes[4],
        shapes[1]
      ));
     return string(abi.encodePacked(
      '<ellipse stroke="black" cx="250" cy="475" rx="30" ry="20" fill="RGB(',
     color1R.toString(),',',
     color1G.toString(),',',
     color1B.toString(),')"/>',
     shapes[shape%6]
      
     ));
  }

  function sword(uint256 number) internal pure virtual returns (string memory){
      uint256 crossguardNumber = (number>>56)&0xFFFFFFFFFFFFFF;
      uint256 gripNumber = (number>>(56*2))&0xFFFFFFFFFFFFFF;
      uint256 pommelNumber = (number>>(56*3))&0xFFFFFFFFFFFFFF;
     return string(abi.encodePacked(
      blade(number),
      crossguard(crossguardNumber),
      grip(gripNumber),
      pommel(pommelNumber)
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
       sword(number),
        '</svg>'
          ));
  }

      
}
