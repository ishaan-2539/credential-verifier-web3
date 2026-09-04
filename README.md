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

---

## 🔌 API Endpoints Reference

## 1. 🩺 Health Check

**GET** `/health`

Verifies that the API is running and that it can successfully connect to the Ethereum node.

---

## 2. 🎓 Issue Credential

**POST** `/credentials/issue`

Hashes the credential payload using **SHA-256** and records the resulting hash on-chain through the smart contract.

### 📥 Request Body

```json
{
  "student_id": "STU-2026-901",
  "degree_name": "B.Tech Computer Science & Engineering",
  "issue_date": "2026-05-15"
}
```

### 📤 Response — `201 Created`

```json
{
  "status": "success",
  "transaction_hash": "0x8f3c...",
  "credential_hash": "0x4a9e..."
}
```

---

## 3. 🔍 Verify Credential

**POST** `/credentials/verify`

Queries the smart contract to verify whether a credential exists and is currently valid.

> 💡 **No gas cost:** This operation only reads blockchain state and does not create a transaction.

### 📥 Request Body

```json
{
  "student_id": "STU-2026-901",
  "degree_name": "B.Tech Computer Science & Engineering",
  "issue_date": "2026-05-15"
}
```

### 📤 Response — `200 OK`

```json
{
  "is_valid": true,
  "issuer": "0x90F79bf6EB2c4f870365E785982E1f101E93b906",
  "issued_at_timestamp": 1778880000,
  "credential_hash": "0x4a9e..."
}
```

---

# 📜 Smart Contract Reference

The core blockchain functionality is implemented in `CredentialRegistry.sol`.

| Function                          | Type                     | Description                                                                     |
| --------------------------------- | ------------------------ | ------------------------------------------------------------------------------- |
| `issueCredential(bytes32 _hash)`  | `external` (`onlyOwner`) | Records a credential hash on-chain along with its timestamp and issuer address. |
| `verifyCredential(bytes32 _hash)` | `external view`          | Returns the credential's validity, issuer address, and block timestamp.         |
| `revokeCredential(bytes32 _hash)` | `external` (`onlyOwner`) | Marks an existing credential as invalid.                                        |

### 🔐 Access Control

* `issueCredential()` can only be called by the contract owner.
* `revokeCredential()` can only be called by the contract owner.
* `verifyCredential()` is publicly readable and does not require gas when called as a read operation.

---

# 🚀 Getting Started

## 📋 Prerequisites

Make sure the following are installed:

* 🐍 **Python 3.10+**
* 🟢 **Node.js**
* 📦 **npm / npx**
* ⛓️ **Ganache** for running a local Ethereum blockchain

---

## 1. 📥 Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/credential-verifier-web3.git
cd credential-verifier-web3
```

---

## 2. ⛓️ Start a Local Blockchain Node

Open a **dedicated terminal window** and launch a local simulated Ethereum node:

```bash
npx ganache --port 8545
```

Keep this terminal running.

Ganache will generate several Ethereum accounts. Locate **Account (0)** and note down its generated **Private Key**.

> ⚠️ **Important:** These accounts are for local development only. Never use Ganache private keys on a real network or with real funds.

---

## 3. 🐍 Set Up the Backend Environment

Open a new terminal and navigate to the backend directory:

```bash
cd backend
```

### Create a Virtual Environment

```bash
python -m venv venv
```

### Activate the Virtual Environment

**Windows:**

```bash
.\venv\Scripts\activate
```

**macOS / Linux:**

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. 📜 Compile & Deploy the Smart Contract

Create a `backend/.env` file:

```env
WEB3_RPC_URL=http://127.0.0.1:8545
ISSUER_PRIVATE_KEY=0xYOUR_GANACHE_PRIVATE_KEY_HERE
CONTRACT_ADDRESS=
```

### ⚙️ Compile the Contract

From the `backend/` directory:

```bash
python compile_contract.py
```

### 🚀 Deploy the Contract

```bash
python deploy_contract.py
```

The deployment script will print the newly deployed **Contract Address**.

Copy this address into your `.env` file:

```env
CONTRACT_ADDRESS=0xYOUR_DEPLOYED_CONTRACT_ADDRESS
```

---

## 5. ⚡ Run the FastAPI Server

From the `backend/` directory:

```bash
uvicorn app.main:app --reload
```

The API server will be available at:

**API:** `http://127.0.0.1:8000`

### 📚 Interactive API Documentation

FastAPI automatically provides Swagger UI:

`http://127.0.0.1:8000/docs`

---

## 6. 🖥️ Launch the Frontend UI

Open:

```text
frontend/index.html
```

directly in your browser.

Alternatively, you can use **VS Code Live Server**.

### 🎓 Issue a Credential

1. Open the **Issue Credential** tab.
2. Enter the:

   * Student ID
   * Degree Name
   * Issue Date
3. Click **Anchor Credential to Ledger**.
4. The backend hashes the credential data and records the hash on-chain.

### 🔍 Verify a Record

1. Switch to the **Verify Student Record** tab.
2. Enter the **exact same credential details**.
3. Submit the verification request.
4. The application queries the blockchain and displays whether the credential is valid.

> 💡 Even a single-character change, extra space, or different date will generate a completely different hash.

---

# ❓ Troubleshooting

## ⛽ `insufficient funds for gas`

### Cause

Your local Ganache node was restarted and generated a new set of accounts and private keys.

### Solution

1. Copy a fresh private key from the active Ganache console.
2. Update `ISSUER_PRIVATE_KEY` in `backend/.env`.
3. Re-run:

```bash
python deploy_contract.py
```

4. Copy the new contract address.
5. Update `CONTRACT_ADDRESS` in `backend/.env`.

---

## ❌ `400 Bad Request` When Issuing a Credential

### Cause

The credential hash already exists on-chain.

The smart contract enforces **unique credentials**, preventing the same credential from being issued twice.

### Solution

Modify one of the credential fields, such as:

* Student ID
* Degree Name
* Issue Date

Then try issuing the credential again.

---

## 🌐 CORS Error in Browser

### Cause

The frontend is being blocked from making requests to the FastAPI backend.

### Solution

Ensure that `CORSMiddleware` is configured correctly in:

```text
backend/app/main.py
```

For example:

```python
from fastapi.middleware.cors import CORSMiddleware
```

and that the middleware is added to the FastAPI application.

---

# 🛡️ Security & Privacy Principles

## 🔒 Privacy by Design

**Personally Identifiable Information (PII) is never written directly to the Ethereum blockchain.**

Instead, the application stores a cryptographic hash of the credential data.

This means the blockchain acts as a **tamper-evident verification layer** without directly exposing the student's personal information.

---

## 🧮 Tamper Evident

The credential data is converted into a **SHA-256 hash** before being recorded on-chain.

Even a tiny modification — such as:

* Changing one character
* Adding a space
* Changing the date
* Modifying the degree name

will produce a completely different hash.

As a result, altered credentials will fail blockchain verification.

---

## 🚫 Revocation Support

The smart contract includes an owner-only:

```solidity
revokeCredential(bytes32 _hash)
```

function.

This allows previously issued credentials to be marked as **invalid** if they were issued incorrectly or become compromised.

---

# 🏗️ How It Works

The overall credential verification flow is:

```text
Student Credential
       │
       ▼
  SHA-256 Hash
       │
       ▼
FastAPI Backend
       │
       ▼
Ethereum Smart Contract
       │
       ▼
Credential Hash Stored On-Chain
       │
       ▼
   Verification
       │
       ▼
Compare Generated Hash
       │
       ▼
 Valid / Invalid
```

### 🔑 Core Principle

> **The blockchain does not store the student's credential itself — it stores a cryptographic proof that can be used to verify the credential's integrity.**

