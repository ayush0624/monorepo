from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):
    DB_URL: str
    JWT_SECRET: str

    model_config = SettingsConfigDict(
        env_file=f"{Path.home()}/.env",
        env_prefix="CONCORD_",
        extra="ignore",
    )


settings = Settings()  # type: ignore
