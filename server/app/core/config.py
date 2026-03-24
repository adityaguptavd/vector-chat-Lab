from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    DATABASE_URL: str
    TEST_DATABASE_URL: str | None = None
    JWT_SECRET: str
    EMBEDDING_MODEL: str
    LOG_LEVEL: str | None = "INFO"
    LLM_API_KEY: str
    LLM_MODEL: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )


settings = Settings()