from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey
from cryptography.hazmat.primitives                import serialization
from cryptography.hazmat.backends                  import default_backend
from pydantic_settings                             import BaseSettings
from pydantic                                      import computed_field
from pathlib                                       import Path

BASE_DIR: Path = Path(__file__).parent.parent


class AuthConfig(BaseSettings):
    database_address: str = "postgresql+asyncpg://hurfy:hurfy0_@localhost:5432/dzshop"

    # tokens
    algorithm: str = "RS256"

    access_token_expire_minutes : int = 15
    refresh_token_expire_minutes: int = 1440

    @computed_field
    @property
    def private_key(self) -> RSAPrivateKey:
        """Gets the private key"""
        with open((BASE_DIR / "certs" / "jwt-private.pem"), "rb") as file:
            return serialization.load_pem_private_key(
                file.read(),
                password=None,
                backend=default_backend(),
            )

    @computed_field
    @property
    def public_key(self) -> RSAPublicKey:
        """Gets the public key"""
        with open((BASE_DIR / "certs" / "jwt-public.pem"), "rb") as file:
            return serialization.load_pem_public_key(
                file.read(),
                backend=default_backend(),
            )


auth_config: AuthConfig = AuthConfig()
