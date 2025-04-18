from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey, RSAPublicNumbers
from hashlib                                       import sha256
from base64                                        import urlsafe_b64encode
from typing                                        import Any


async def create_jwk(pub_key: RSAPublicKey) -> dict[str, Any]:
    """Creates a JWK token"""
    numbers: RSAPublicNumbers = pub_key.public_numbers()

    # To bytes
    n_bytes: bytes = numbers.n.to_bytes((numbers.n.bit_length() + 7) // 8, byteorder='big')
    e_bytes: bytes = numbers.e.to_bytes((numbers.e.bit_length() + 7) // 8, byteorder='big')

    return {
        "kty": "RSA",
        "alg": "RS256",
        "use": "sig",
        "kid": sha256(n_bytes).hexdigest()[:16],
        "n"  : urlsafe_b64encode(n_bytes).decode("utf-8").rstrip("="),
        "e"  : urlsafe_b64encode(e_bytes).decode("utf-8").rstrip("="),
    }
