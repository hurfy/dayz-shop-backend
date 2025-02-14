from datetime  import timedelta
from typing    import Any
from enum      import Enum

from ...config import auth_config
from ...errors import InvalidToken
from .encoder  import encode_jwt
from .decoder  import decode_jwt

class TokenType(str, Enum):
    access : str = "access"
    refresh: str = "refresh"


async def create_jwt(
        token_type: TokenType,
        steam_id  : str,
        expires_in: timedelta,
):
    """Creates a JWT token with the specified type and steamid"""
    payload: dict[str, Any] = {
        "type"   : token_type.value,
        "steamid": steam_id,
    }

    return await encode_jwt(
        payload=payload,
        expires_in=expires_in,
    )


async def create_access_token(steamid: str) -> str:
    """Creates a JWT access token"""
    return await create_jwt(
        token_type=TokenType.access,
        steam_id=steamid,
        expires_in=timedelta(minutes=auth_config.access_token_expire_minutes),
    )


async def create_refresh_token(steamid: str) -> str:
    """Creates a JWT refresh token"""
    return await create_jwt(
        token_type=TokenType.refresh,
        steam_id=steamid,
        expires_in=timedelta(minutes=auth_config.refresh_token_expire_minutes),
    )


async def get_token_type(token: str) -> TokenType:
    """Gets the type of token"""
    decoded: dict[str, Any] = decode_jwt(token)

    if decoded.get("token_type", None) is None:
        raise InvalidToken()

    return decoded["token_type"]


async def is_access_token(token: str) -> bool:
    """Checks if the token type is access"""
    return await get_token_type(token) == TokenType.access
