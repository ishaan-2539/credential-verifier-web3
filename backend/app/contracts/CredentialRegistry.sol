// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract CredentialRegistry {
    address public owner;

    struct Credential {
        bytes32 credentialHash;
        address issuer;
        uint256 issuedAt;
        bool isValid;
    }

    mapping(bytes32 => Credential) public credentials;

    event CredentialIssued(bytes32 indexed credentialHash, address indexed issuer, uint256 issuedAt);
    event CredentialRevoked(bytes32 indexed credentialHash);

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can perform this action");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    function issueCredential(bytes32 _credentialHash) external onlyOwner {
        require(credentials[_credentialHash].issuedAt == 0, "Credential already exists");

        credentials[_credentialHash] = Credential({
            credentialHash: _credentialHash,
            issuer: msg.sender,
            issuedAt: block.timestamp,
            isValid: true
        });

        emit CredentialIssued(_credentialHash, msg.sender, block.timestamp);
    }

    function verifyCredential(bytes32 _credentialHash) external view returns (bool isValid, address issuer, uint256 issuedAt) {
        Credential memory cred = credentials[_credentialHash];
        return (cred.isValid, cred.issuer, cred.issuedAt);
    }

    function revokeCredential(bytes32 _credentialHash) external onlyOwner {
        require(credentials[_credentialHash].issuedAt != 0, "Credential does not exist");
        credentials[_credentialHash].isValid = false;

        emit CredentialRevoked(_credentialHash);
    }
}