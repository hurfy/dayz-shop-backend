from pydantic_settings import BaseSettings


class UsersConfig(BaseSettings):
    database_address: str = "postgresql+asyncpg://hurfy:hurfy@localhost/dzshop"


users_config: UsersConfig = UsersConfig()
