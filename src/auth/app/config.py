from pydantic_settings import BaseSettings
from pathlib           import Path


BASE_DIR: Path = Path(__file__).parent.parent


class AuthConfig(BaseSettings):
    private_key: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key : Path = BASE_DIR / "certs" / "jwt-public.pem"

    algorithm: str = "RS256"

    access_token_expire_minutes : int = 15
    refresh_token_expire_minutes: int = 1440


auth_config: AuthConfig = AuthConfig()
