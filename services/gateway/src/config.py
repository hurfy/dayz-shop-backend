from pydantic_settings import BaseSettings, SettingsConfigDict


class GatewayConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../.env",
        env_file_encoding="utf-8",
    )

    database_address: str = "postgresql+asyncpg://hurfy:hurfy@localhost/dzshop"
    steam_api_key   : str  # TODO: FIX - missing when generate alembic revision

    # services
    auth_service_address : str = "http://127.0.0.1:8001/auth"
    users_service_address: str = "http://127.0.0.1:8002/users"


gateway_config: GatewayConfig = GatewayConfig()
