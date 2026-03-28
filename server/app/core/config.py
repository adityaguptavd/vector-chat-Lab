from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal


class Settings(BaseSettings):

    DATABASE_URL: str
    TEST_DATABASE_URL: str | None = None
    JWT_SECRET: str
    EMBEDDING_MODEL: str
    LOG_LEVEL: str | None = "INFO"
    LLM_API_KEY: str
    LLM_MODEL: str
    ENV: Literal["dev", "prod"]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )


settings = Settings()