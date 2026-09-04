import hashlib
from app.clients.blockchain_client import blockchain_client

class VerificationService:
    @staticmethod
    def generate_credential_hash(student_id: str, degree_name: str, issue_date: str) -> bytes:
        """
        Creates a deterministic SHA-256 hash of student credential data.
        Returns bytes32 format expected by Solidity.
        """
        raw_data = f"{student_id}:{degree_name}:{issue_date}"
        hash_hex = hashlib.sha256(raw_data.encode("utf-8")).hexdigest()
        return bytes.fromhex(hash_hex)

    def issue_credential(self, student_id: str, degree_name: str, issue_date: str) -> dict:
        credential_bytes = self.generate_credential_hash(student_id, degree_name, issue_date)
        tx_hash = blockchain_client.issue_credential(credential_bytes)
        
        return {
            "status": "success",
            "transaction_hash": tx_hash,
            "credential_hash": f"0x{credential_bytes.hex()}"
        }

    def verify_credential(self, student_id: str, degree_name: str, issue_date: str) -> dict:
        credential_bytes = self.generate_credential_hash(student_id, degree_name, issue_date)
        result = blockchain_client.verify_credential(credential_bytes)
        
        return {
            "is_valid": result["is_valid"],
            "issuer": result["issuer"],
            "issued_at_timestamp": result["issued_at"],
            "credential_hash": f"0x{credential_bytes.hex()}"
        }

verification_service = VerificationService()