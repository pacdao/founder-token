// SPDX-License-Identifier: MIT
pragma solidity 0.6.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";

contract PACFounder is ERC721 {

/* Variables */
    uint256 public minPrice = 100000000000000;
    address payable private beneficiary;
    uint256 public currentId;
    string defaultMetadata = "QmcnEZQiGVzPonWS2MENbdY8DkwhWcCW7YBQNk5yHYF112";

    constructor (address payable _beneficiary) public ERC721 ("PACDAO FOUNDER", "PAC-F"){
		beneficiary = _beneficiary;
		_setBaseURI("ipfs://");

    }

/* Payable Functions */
    function mint() public payable
	{
		require(msg.value >= minPrice, "Must pay more");
		currentId += 1;
		_safeMint(msg.sender, currentId);
		_setTokenURI(currentId, defaultMetadata);
		uint _target = minPrice * 1075000000000000000 / 1e18;
		if(_target - minPrice < 1e14) {
			_target = minPrice + 1e14;
		}
		if(currentId < 20) {
			currentId += 1;
			_safeMint(beneficiary, currentId);
			_setTokenURI(currentId, defaultMetadata);
		}

		if(msg.value > _target) {
			minPrice = msg.value + 1e14;
		} else {
			minPrice = _target;
		}
		minPrice = minPrice / 1e14 * 1e14;
	}

/* Nonpayable Functions */
	function withdraw() public 
	{
		beneficiary.transfer(address(this).balance);
	}

/* Admin Functions */
	function updateBeneficiary(address payable _newBeneficiary) public 
	{		
		require(msg.sender == beneficiary);
		beneficiary = _newBeneficiary;
	}
	function setTokenUri(uint256 _tokenId, string memory _newUri) public 
	{
		require(msg.sender == beneficiary);
		_setTokenURI(_tokenId, _newUri);
	}
	function setDefaultMetadata(string memory _newUri) public 
	{
		require(msg.sender == beneficiary);
		defaultMetadata = _newUri;
	}

/* Fallback Functions */
	receive() external payable { }
	fallback() external payable { }

}
