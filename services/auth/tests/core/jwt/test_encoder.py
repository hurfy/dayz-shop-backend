import pytest

from re import match


@pytest.mark.asyncio
async def test_encode_jwt(jwt_token: str, jwt_re_pattern: str) -> None:
    """test_encode_jwt ..."""
    assert jwt_token is not None
    assert isinstance(jwt_token, str)
    assert match(jwt_re_pattern, jwt_token)
