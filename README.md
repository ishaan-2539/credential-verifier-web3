# Academic Credential Registry

> A decentralized, privacy-first academic credential verification platform built with **FastAPI**, **Solidity**, and **Ethereum Smart Contracts**.

---

## 📌 Overview

The **Academic Credential Registry** provides educational institutions with a tamper-proof method to issue and verify student degrees, diplomas, and certifications on-chain.

Instead of storing sensitive personally identifiable information (PII) on a public blockchain, this platform converts student credentials into deterministic **SHA-256 cryptographic hashes** (`bytes32`). Only the cryptographic signature is anchored on-chain, ensuring zero data leakage while offering instant, free, and mathematical proof of authenticity for employers and universities.

---

## 🛠️ Tech Stack

### **Backend & Web3 Integration**
* **Python 3.10+ & FastAPI:** Asynchronous REST API architecture providing fast execution and auto-generated Swagger documentation.
* **Web3.py:** Ethereum JSON-RPC client interface for transaction signing, smart contract interaction, and gas estimation.
* **Pydantic v2 & Pydantic Settings:** Strict data modeling, input validation, and fail-fast environment management (`.env`).
* **py-solc-x:** Automated local Solidity smart contract compilation.

### **Blockchain & Smart Contracts**
* **Solidity (`^0.8.20`):** Immutable smart contract (`CredentialRegistry.sol`) storing credential hashes, issuer addresses, timestamps, and validity flags.
* **Ganache / Anvil:** Local Ethereum node simulation for instant zero-cost testing.

### **Frontend**
* **HTML5 & Vanilla JavaScript:** Lightweight, zero-build-step client interface utilizing native `fetch` requests.
* **Tailwind CSS:** Custom dark, slate-themed workspace styled with custom typography (*Plus Jakarta Sans*, *Instrument Serif*, and *JetBrains Mono*).

---

## 📂 System Architecture

```text
credential-verifier-web3/
├── backend/
│   ├── app/
│   │   ├── clients/
│   │   │   └── blockchain_client.py   # Web3.py RPC client wrapper
│   │   ├── contracts/
│   │   │   ├── CredentialRegistry.sol  # Solidity Smart Contract
│   │   │   └── compiled_contract.json # Compiled artifact (ABI + Bytecode)
│   │   ├── routers/
│   │   │   └── verification_router.py  # FastAPI APIRouter endpoints
│   │   ├── services/
│   │   │   └── verification_service.py # SHA-256 Hashing & business logic
│   │   ├── config.py                   # Pydantic Settings (.env handling)
│   │   └── main.py                     # FastAPI application entrypoint
│   ├── .env                            # Local secrets (Private keys, RPC URLs)
│   ├── compile_contract.py             # Script to compile Solidity contract
│   ├── deploy_contract.py              # Script to deploy contract to network
│   └── requirements.txt
├── frontend/
│   └── index.html                      # Unified dark studio UI
├── .gitignore
└── README.md