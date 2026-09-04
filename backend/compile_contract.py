import json
from pathlib import Path
from solcx import compile_standard, install_solc

SOLC_VERSION = "0.8.20"

def compile_credential_contract():
    print(f"Installing solc version {SOLC_VERSION}...")
    install_solc(SOLC_VERSION)

    contract_path = Path(__file__).parent / "app" / "contracts" / "CredentialRegistry.sol"
    contract_source = contract_path.read_text()

    print("Compiling CredentialRegistry.sol...")
    compiled_sol = compile_standard(
        {
            "language": "Solidity",
            "sources": {"CredentialRegistry.sol": {"content": contract_source}},
            "settings": {
                "outputSelection": {
                    "*": {
                        "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                    }
                }
            },
        },
        solc_version=SOLC_VERSION,
    )

    output_path = Path(__file__).parent / "app" / "contracts" / "compiled_contract.json"
    output_path.write_text(json.dumps(compiled_sol, indent=2))
    print(f"Compilation successful! Output saved to {output_path}")

if __name__ == "__main__":
    compile_credential_contract()