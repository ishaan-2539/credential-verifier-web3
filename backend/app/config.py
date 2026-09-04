from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # RPC URL for connecting to the Ethereum network or local node
    WEB3_RPC_URL: str = "http://127.0.0.1:8545"
    
    # Private Key of the Issuer account (for signing write transactions)
    ISSUER_PRIVATE_KEY: str = ""
    
    # Deployed CredentialRegistry contract address (0x...)
    CONTRACT_ADDRESS: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()