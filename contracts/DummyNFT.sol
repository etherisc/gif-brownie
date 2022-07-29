// SPDX-License-Identifier: Apache-2.0
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC721/ERC721.sol";

contract DummyNFT is 
    ERC721,
    Ownable
{
    string public constant NAME = "Dummy NFT";
    string public constant SYMBOL = "DNT";

    uint256 _tokens;

    constructor() ERC721(NAME, SYMBOL) Ownable() { }

    function mint(address to) 
        external 
        onlyOwner
        returns(uint256 tokenId)
    {
        _tokens++;
        tokenId = _tokens;
        _safeMint(to, tokenId);
    }

    function tokens() external view returns(uint256) {
        return _tokens;
    }
}
