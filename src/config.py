from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # FastAPI
    FASTAPI_HOST     : str = None
    FASTAPI_PORT     : str = None

    # PostgreSQL
    POSTGRES_PASSWORD: str = None
    POSTGRES_USER    : str = None
    POSTGRES_DB      : str = None
    POSTGRES_PORT    : str = None

    model_config = SettingsConfigDict(env_file="../.env")

    @property
    def DATABASE_URL_asyncpg(self) -> str:
        """DATABASE_URL_asyncpg ..."""
        return (
            f"postgresql+asyncpg://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@db:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


settings = Settings()
