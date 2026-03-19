from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    JWT_SECRET: str
    JWT_ALG: str
    JWT_EXPIRY_MINUTES: int

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent.parent / ".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )

settings = Settings()