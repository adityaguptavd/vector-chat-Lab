from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    DATABASE_URL: str
    TEST_DATABASE_URL: str | None = None
    JWT_SECRET: str
    EMBEDDING_MODEL: str
    LOG_LEVEL: str | None = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )


settings = Settings()