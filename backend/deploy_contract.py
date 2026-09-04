from web3 import Web3
from app.config import settings
import json
from pathlib import Path

def deploy():
    w3 = Web3(Web3.HTTPProvider(settings.WEB3_RPC_URL))
    if not w3.is_connected():
        print("Error: Cannot connect to local RPC node at", settings.WEB3_RPC_URL)
        return

    account = w3.eth.account.from_key(settings.ISSUER_PRIVATE_KEY)

    artifact_path = Path(__file__).parent / "app" / "contracts" / "compiled_contract.json"
    with open(artifact_path, "r") as f:
        compiled_json = json.load(f)

    contract_data = compiled_json["contracts"]["CredentialRegistry.sol"]["CredentialRegistry"]
    abi = contract_data["abi"]
    bytecode = contract_data["evm"]["bytecode"]["object"]

    Contract = w3.eth.contract(abi=abi, bytecode=bytecode)

    tx = Contract.constructor().build_transaction({
        "from": account.address,
        "nonce": w3.eth.get_transaction_count(account.address),
        "gasPrice": w3.eth.gas_price
    })

    signed_tx = w3.eth.account.sign_transaction(tx, settings.ISSUER_PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    print(f"\n Contract Deployed Successfully!")
    print(f"Contract Address: {receipt['contractAddress']}")
    print("\nCopy this Contract Address into your backend/.env file under CONTRACT_ADDRESS=")

if __name__ == "__main__":
    deploy()