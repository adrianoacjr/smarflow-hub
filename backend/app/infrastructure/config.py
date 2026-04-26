from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    OPENAI_API_KEY: str
    OPENAI_TIMEOUT: int = 20
    OPENAI_MAX_RETRIES: int = 3
    OPENAI_RETRY_BACKOFF: float = 1.5
    SECRET_KEY: str
    ACCESS_TOKEN_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    WHATSAPP_TOKEN: str
    WHATSAPP_PHONE_NUMBER_ID: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
