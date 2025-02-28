from datetime import datetime, timedelta, UTC
from typing   import Any
from uuid     import uuid4
from jwt      import encode

from config   import auth_config


async def encode_jwt(
        expires_in: timedelta,
        payload   : dict[str, Any],
        algorithm : str = auth_config.algorithm,
) -> str:
    """Encodes the info into a JWT token"""
    to_encode: dict[str, Any] = payload.copy()

    # Time
    now   : datetime = datetime.now(UTC)
    expire: datetime = now + expires_in

    # Update encode data
    to_encode.update({
        "exp": expire.timestamp(),
        "iat": now.timestamp(),
        "jti": str(uuid4()),
        "iss": "dzshop-auth",
    })

    return encode(
        to_encode,
        auth_config.private_key,
        algorithm=algorithm,
    )
