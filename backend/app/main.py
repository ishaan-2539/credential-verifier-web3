from fastapi import FastAPI
from app.routers import verification_router
from app.clients.blockchain_client import blockchain_client

app = FastAPI(
    title="Web3 Credential Verifier",
    version="1.0.0",
    description="Decentralized credential verification system built with FastAPI and Solidity."
)

app.include_router(verification_router.router)

@app.get("/health")
def health_check():
    connected = blockchain_client.is_connected()
    return {
        "status": "healthy" if connected else "degraded",
        "blockchain_connected": connected
    }