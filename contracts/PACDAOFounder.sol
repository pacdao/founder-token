// SPDX-License-Identifier: MIT
pragma solidity 0.6.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
//import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract PACFounder is ERC721 {
    uint256 public minPrice;
    uint256 public minStep;
    address payable private beneficiary;
    uint256 public currentId;
    string defaultMetadata = "QmcnEZQiGVzPonWS2MENbdY8DkwhWcCW7YBQNk5yHYF112";

    constructor (uint256 _floorPrice, uint256 _minStep, address payable _beneficiary) public ERC721 ("PACDAO FOUNDER", "PAC-F"){
		minPrice = _floorPrice;
		minStep = _minStep;
		beneficiary = _beneficiary;
		_setBaseURI("ipfs://");
		for(uint i = 1; i <= 10; i++) {
			_safeMint(beneficiary, i);
		}
        	currentId = 10;
    }
    function mint() public payable
	{
		require(msg.value >= minPrice, "Must pay more");
		currentId += 1;
		_safeMint(msg.sender, currentId);
		_setTokenURI(currentId, defaultMetadata);
		uint _target = minPrice * 1075000000000000000 / 1e18;
		if(_target - minPrice < minStep) {
			_target = minPrice + minStep;
		}

		if(msg.value > _target) {
			minPrice = msg.value + minStep;
		} else {
			minPrice = _target;
		}
		minPrice = minPrice / 1e14 * 1e14;
	}
	function updateBeneficiary(address payable _newBeneficiary) public {
		require(msg.sender == beneficiary, "Not allowed");
		beneficiary = _newBeneficiary;
	}
	function setTokenUri(uint256 _tokenId, string memory _newUri) public {
		require(msg.sender == beneficiary, "Not allowed");
		_setTokenURI(_tokenId, _newUri);

	}
	function setDefaultMetadata(string memory _newUri) public {
		require(msg.sender == beneficiary, "Not allowed");
		defaultMetadata = _newUri;

	}

function withdraw() public
{
	beneficiary.transfer(address(this).balance);
}

receive() external payable { }
fallback() external payable { }

/*
function recoverERC20(address tokenAddress, uint256 tokenAmount) public {
	IERC20(tokenAddress).transfer(beneficiary, tokenAmount);
}
*/
}
