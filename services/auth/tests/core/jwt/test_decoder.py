import pytest

from jwt.exceptions import ExpiredSignatureError
from typing         import Any

from core.jwt       import decode_jwt


@pytest.mark.asyncio
async def test_decode_jwt(jwt_token: str, steam_id: str) -> None:
    """test_decode_jwt ..."""
    decoded_token: dict[str, Any] = await decode_jwt(jwt_token)

    assert decoded_token is not None
    assert isinstance(decoded_token, dict)

    # Steam
    assert decoded_token["steamid"] == steam_id

    # Has fields
    for field in {"steamid", "exp", "iat", "jti"}:
        assert field in decoded_token


@pytest.mark.asyncio
async def test_decode_jwt_exp(jwt_token_exp: str) -> None:
    """test_decode_jwt_exp ..."""
    with pytest.raises(ExpiredSignatureError):
        await decode_jwt(jwt_token_exp)
