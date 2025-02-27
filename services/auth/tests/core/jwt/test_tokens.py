import pytest

from dzshop.enums import RoleType
from datetime     import timedelta
from typing       import Any
from re           import match

from core.jwt     import TokenType, create_jwt, create_access_token, create_refresh_token, decode_jwt


async def assert_jwt_validity(
        token: str,
        token_type: TokenType,
        role_type: RoleType,
        jwt_re_pattern: str,
        steam_id: str
) -> None:
    """Helper function to validate JWT format and decode content"""
    assert token is not None
    assert isinstance(token, str)
    assert match(jwt_re_pattern, token)

    decoded: dict[str, Any] = await decode_jwt(token)
    assert decoded is not None

    assert decoded["type"] == token_type
    assert decoded["sub"] == steam_id
    assert decoded["role"] == role_type


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "token_type, role_type",
    [
        (TokenType.access, RoleType.admin),
        (TokenType.access, RoleType.user),
    ]
)
async def test_create_jwt(token_type: TokenType, role_type: RoleType, jwt_re_pattern: str, steam_id: str) -> None:
    """test_create_jwt ..."""
    access_token: str = await create_jwt(
        token_type,
        steam_id,
        role_type,
        timedelta(minutes=5),
    )

    await assert_jwt_validity(access_token, token_type, role_type, jwt_re_pattern, steam_id)


@pytest.mark.asyncio
async def test_create_access_token(jwt_re_pattern: str, steam_id: str) -> None:
    """test_create_access_token ..."""
    access_token: str = await create_access_token(steamid=steam_id, role=RoleType.user)
    await assert_jwt_validity(access_token, TokenType.access, RoleType.user, jwt_re_pattern, steam_id)


@pytest.mark.asyncio
async def test_create_refresh_token(jwt_re_pattern: str, steam_id: str) -> None:
    """test_create_refresh_token ..."""
    refresh_token: str = await create_refresh_token(steamid=steam_id, role=RoleType.user)
    await assert_jwt_validity(refresh_token, TokenType.refresh, RoleType.user, jwt_re_pattern, steam_id)
