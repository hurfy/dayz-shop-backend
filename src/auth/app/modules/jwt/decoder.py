from typing    import Any
from jwt       import decode

from ...config import auth_config


async def decode_jwt(
        token    : str | bytes,
        algorithm: str = auth_config.algorithm
) -> dict[str, Any]:
    """Decodes a JWT token"""
    return decode(
        token,
        auth_config.public_key.read_text(),
        algorithms=[algorithm],
    )
