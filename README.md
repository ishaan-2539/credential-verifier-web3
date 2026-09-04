# 🔐 Credential Verifier Web3

A blockchain-based credential verification system that uses **SHA-256 hashing**, **Ethereum smart contracts**, and a **FastAPI backend** to issue, verify, and revoke academic credentials in a tamper-evident manner.

The system stores **credential hashes rather than Personally Identifiable Information (PII)** directly on the blockchain, allowing credentials to be verified without exposing the underlying student information.

---

# ✨ Features

* 🎓 **Credential Issuance** — Hashes credential information using SHA-256 and records the hash on-chain.
* 🔍 **Credential Verification** — Verifies credentials directly against Ethereum smart contract state.
* 🚫 **Credential Revocation** — Allows the contract owner to invalidate previously issued credentials.
* 🛡️ **Privacy by Design** — Student information is never stored directly on the blockchain.
* 🧮 **Tamper Detection** — Any modification to the credential data results in a different hash.
* ⛓️ **Blockchain-backed Integrity** — Credential records are anchored to an Ethereum blockchain.
* ⚡ **Gas-free Verification** — Verification is a read-only blockchain operation and does not require gas.
* 🌐 **FastAPI Backend** — Provides REST API endpoints for interacting with the blockchain.
* 🖥️ **Web Frontend** — Provides interfaces for issuing and verifying credentials.

---

# 🏗️ System Architecture

```text
┌──────────────────────┐
│   Student Credential │
│  ID / Degree / Date  │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│      SHA-256 Hash    │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│    FastAPI Backend   │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Ethereum Smart       │
│ Contract             │
│ CredentialRegistry   │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Credential Hash      │
│ Stored On-Chain      │
└──────────────────────┘
```

For verification:

```text
Credential Details
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
Compare Stored Hash
       │
       ▼
 ┌───────────────┐
 │ Valid /       │
 │ Invalid       │
 └───────────────┘
```

---

# 🔌 API Endpoints Reference

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

The core blockchain functionality is implemented in:

```text
CredentialRegistry.sol
```

## 📋 Contract Functions

| Function                          | Type                     | Description                                                                     |
| --------------------------------- | ------------------------ | ------------------------------------------------------------------------------- |
| `issueCredential(bytes32 _hash)`  | `external` (`onlyOwner`) | Records a credential hash on-chain along with its timestamp and issuer address. |
| `verifyCredential(bytes32 _hash)` | `external view`          | Returns the credential's validity, issuer address, and block timestamp.         |
| `revokeCredential(bytes32 _hash)` | `external` (`onlyOwner`) | Marks an existing credential as invalid.                                        |

## 🔐 Access Control

* `issueCredential()` can only be called by the **contract owner**.
* `revokeCredential()` can only be called by the **contract owner**.
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

#### 🪟 Windows

```bash
.\venv\Scripts\activate
```

#### 🍎 macOS / 🐧 Linux

```bash
source venv/bin/activate
```

### 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. 📜 Compile & Deploy the Smart Contract

Create a:

```text
backend/.env
```

file with the following configuration:

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

Copy the printed address into your `.env` file:

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

```text
http://127.0.0.1:8000
```

### 📚 Interactive API Documentation

FastAPI automatically provides Swagger UI at:

```text
http://127.0.0.1:8000/docs
```

---

## 6. 🖥️ Launch the Frontend UI

Open:

```text
frontend/index.html
```

directly in your web browser.

Alternatively, you can use **VS Code Live Server**.

---

# 🎓 Using the Application

## 📝 Issue a Credential

1. Open the **Issue Credential** tab.
2. Enter the:

   * Student ID
   * Degree Name
   * Issue Date
3. Click **Anchor Credential to Ledger**.
4. The backend hashes the credential data using SHA-256.
5. The resulting credential hash is recorded on-chain.

---

## 🔍 Verify a Student Record

1. Switch to the **Verify Student Record** tab.
2. Enter the **exact same credential details**.
3. Submit the verification request.
4. The application queries the blockchain.
5. The application displays whether the credential is valid.

> 💡 **Important:** Even a single-character change, extra space, or different date will generate a completely different hash.

---

# ❓ Troubleshooting

## ⛽ `insufficient funds for gas`

### Cause

Your local Ganache node was restarted and generated a new set of accounts and private keys.

### Solution

1. Copy a fresh private key from the active Ganache console.
2. Update `ISSUER_PRIVATE_KEY` in `backend/.env`.
3. Re-run the contract deployment:

```bash
python deploy_contract.py
```

4. Copy the newly generated contract address.
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

and make sure the middleware is added to the FastAPI application.

---

# 🛡️ Security & Privacy Principles

## 🔒 Privacy by Design

**Personally Identifiable Information (PII) is never written directly to the Ethereum blockchain.**

Instead, the application stores a cryptographic hash of the credential data.

This allows the blockchain to act as a **tamper-evident verification layer** without directly exposing the student's personal information.

---

## 🧮 Tamper Evident

The credential data is converted into a **SHA-256 hash** before being recorded on-chain.

Even a tiny modification, such as:

* Changing one character
* Adding a space
* Changing the date
* Modifying the degree name

will produce a completely different hash.

As a result, altered credentials will fail blockchain verification.

---

## 🚫 Revocation Support

The smart contract includes the following owner-only function:

```solidity
revokeCredential(bytes32 _hash)
```

This allows previously issued credentials to be marked as **invalid** if they were issued incorrectly or become compromised.

---

# 🔑 Core Principle

> **The blockchain does not store the student's credential itself — it stores a cryptographic proof that can be used to verify the credential's integrity.**

The combination of **SHA-256 hashing + Ethereum smart contracts + FastAPI** provides a tamper-evident mechanism for issuing and verifying academic credentials while keeping the underlying student information off-chain.

---

# 🧪 Example Credential Flow

### 1️⃣ Credential Issued

```text
Student ID:
STU-2026-901

Degree:
B.Tech Computer Science & Engineering

Issue Date:
2026-05-15
```

⬇️

### 2️⃣ SHA-256 Hash Generated

```text
0x4a9e...
```

⬇️

### 3️⃣ Hash Recorded On-Chain

```text
Ethereum Smart Contract
        │
        ├── Credential Hash
        ├── Issuer Address
        └── Timestamp
```

⬇️

### 4️⃣ Credential Verified

The same credential details are hashed again.

```text
Generated Hash
      │
      ▼
Compare With
On-Chain Hash
      │
      ▼
Valid ✅
```

If any credential information has been modified:

```text
Modified Credential
        │
        ▼
Different SHA-256 Hash
        │
        ▼
No Matching Record
        │
        ▼
Invalid ❌
```

---

# 📁 Project Structure

A typical project structure is:

```text
credential-verifier-web3/
│
├── backend/
│   ├── app/
│   │   └── main.py
│   │
│   ├── .env
│   ├── requirements.txt
│   ├── compile_contract.py
│   └── deploy_contract.py
│
├── frontend/
│   └── index.html
│
└── contracts/
    └── CredentialRegistry.sol
```

> 📌 The exact structure may vary depending on the repository implementation.

---

# ⚠️ Development Notes

* Ganache is used as a **local simulated Ethereum blockchain**.
* Restarting Ganache generates a new set of accounts and private keys.
* When Ganache is restarted, the smart contract must be deployed again.
* The corresponding `ISSUER_PRIVATE_KEY` and `CONTRACT_ADDRESS` must then be updated in `backend/.env`.
* The blockchain stores the **credential hash**, not the student's raw credential information.
* Verification is a read-only operation and therefore does not require gas.
* Credential issuance and revocation are blockchain transactions and therefore require gas.
* Credential hashes are unique, so the same credential cannot be issued twice.

---

# 🛡️ Security Warning

The `.env` file contains the issuer's private key:

```env
ISSUER_PRIVATE_KEY=0xYOUR_GANACHE_PRIVATE_KEY_HERE
```

Never commit `.env` or real private keys to GitHub.

For local development, use Ganache-generated accounts only. Never use private keys containing real funds or production credentials.

---

# 🎯 Summary

**Credential Verifier Web3** provides a simple blockchain-based approach to academic credential verification:

```text
        🎓 Credential
              │
              ▼
       🧮 SHA-256 Hash
              │
              ▼
       ⚡ FastAPI Backend
              │
              ▼
       ⛓️ Ethereum Contract
              │
              ▼
      🔐 Hash Stored On-Chain
              │
              ▼
        🔍 Verification
              │
       ┌──────┴──────┐
       ▼             ▼
   ✅ Valid       ❌ Invalid
```

The system demonstrates how blockchain can be used as a **tamper-evident trust layer** while keeping sensitive credential information off-chain.
