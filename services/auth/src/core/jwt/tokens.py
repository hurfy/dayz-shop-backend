from dzshop.enums     import RoleType
from datetime         import timedelta
from typing           import Any

from core.jwt.decoder import decode_jwt
from core.jwt.encoder import encode_jwt
from core.errors      import InvalidToken
from core.enums       import TokenType
from config           import auth_config


async def create_jwt(
        token_type: TokenType,
        steam_id  : str,
        role      : RoleType,
        expires_in: timedelta,
):
    """Creates a JWT token with the specified type and steamid"""
    payload: dict[str, Any] = {
        "type": token_type.value,
        "role": role,
        "sub" : steam_id,
    }

    return await encode_jwt(
        payload=payload,
        expires_in=expires_in,
    )


async def create_access_token(steamid: str, role: RoleType) -> str:
    """Creates a JWT access token"""
    return await create_jwt(
        token_type=TokenType.access,
        steam_id=steamid,
        role=role,
        expires_in=timedelta(minutes=auth_config.access_token_expire_minutes),
    )


async def create_refresh_token(steamid: str, role: RoleType) -> str:
    """Creates a JWT refresh token"""
    return await create_jwt(
        token_type=TokenType.refresh,
        steam_id=steamid,
        role=role,
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
