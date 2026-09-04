import json
from pathlib import Path
from web3 import Web3
from app.config import settings

class BlockchainClient:
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(settings.WEB3_RPC_URL))
        self.contract = None

        if settings.CONTRACT_ADDRESS:
            self.load_contract(settings.CONTRACT_ADDRESS)

    def load_contract(self, contract_address: str):
        """Loads the compiled contract ABI and sets up the Web3 contract object."""
        artifact_path = Path(__file__).parent.parent / "contracts" / "compiled_contract.json"
        
        if not artifact_path.exists():
            raise FileNotFoundError("Compiled contract artifact not found. Run compile_contract.py first.")

        with open(artifact_path, "r") as f:
            compiled_json = json.load(f)

        # Extract ABI from compiled artifact
        contract_data = compiled_json["contracts"]["CredentialRegistry.sol"]["CredentialRegistry"]
        abi = contract_data["abi"]

        checksum_address = self.w3.to_checksum_address(contract_address)
        self.contract = self.w3.eth.contract(address=checksum_address, abi=abi)

    def is_connected(self) -> bool:
        """Checks connection to the blockchain node."""
        return self.w3.is_connected()

    def verify_credential(self, credential_hash_bytes: bytes) -> dict:
        """Reads credential state on-chain (Free / No Gas cost)."""
        if not self.contract:
            raise ValueError("Contract not loaded. Provide CONTRACT_ADDRESS in settings.")

        is_valid, issuer, issued_at = self.contract.functions.verifyCredential(credential_hash_bytes).call()
        return {
            "is_valid": is_valid,
            "issuer": issuer,
            "issued_at": issued_at
        }

    def issue_credential(self, credential_hash_bytes: bytes) -> str:
        """Signs and sends a transaction to record a credential on-chain (Requires Gas)."""
        if not self.contract:
            raise ValueError("Contract not loaded. Provide CONTRACT_ADDRESS in settings.")
        if not settings.ISSUER_PRIVATE_KEY:
            raise ValueError("ISSUER_PRIVATE_KEY is missing in settings.")

        account = self.w3.eth.account.from_key(settings.ISSUER_PRIVATE_KEY)
        nonce = self.w3.eth.get_transaction_count(account.address)

        # Build transaction
        tx = self.contract.functions.issueCredential(credential_hash_bytes).build_transaction({
            "from": account.address,
            "nonce": nonce,
            "gasPrice": self.w3.eth.gas_price,
        })

        # Sign and broadcast transaction
        signed_tx = self.w3.eth.account.sign_transaction(tx, settings.ISSUER_PRIVATE_KEY)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)

        # Wait for transaction receipt (block inclusion)
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return receipt["transactionHash"].hex()

# Global Client Instance
blockchain_client = BlockchainClient()