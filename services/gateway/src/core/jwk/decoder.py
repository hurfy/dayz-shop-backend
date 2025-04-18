from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicNumbers
from cryptography.hazmat.primitives.asymmetric     import rsa
from cryptography.hazmat.backends                  import default_backend
from dzshop.dto.jwks                               import JwksDTO
from base64                                        import urlsafe_b64decode
from typing                                        import Any

from core.jwk.fetcher                              import fetch_jwks


async def decode_jwk() -> rsa.RSAPublicKey:
    """decode_jwk ..."""
    jwks: JwksDTO        = await fetch_jwks()
    jwk : dict[str, Any] = jwks.keys[0]

    n: int = int.from_bytes(urlsafe_b64decode(jwk["n"] + "=="), byteorder="big")
    e: int = int.from_bytes(urlsafe_b64decode(jwk["e"] + "=="), byteorder="big")

    return RSAPublicNumbers(e, n).public_key(default_backend())
