from pydantic_settings import BaseSettings


class GatewayConfig(BaseSettings):
    database_address: str = "postgresql+asyncpg://hurfy:hurfy0_@localhost/dzshop"

    # services
    auth_service_address: str = "http://127.0.0.1:8001/auth/create"


gateway_config: GatewayConfig = GatewayConfig()
