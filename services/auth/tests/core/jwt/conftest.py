import pytest_asyncio

from datetime import timedelta
from typing   import Any

from core.jwt import encode_jwt


@pytest_asyncio.fixture(scope="package")
async def jwt_re_pattern() -> str:
    """jwt_re_pattern ..."""
    return r"(^[\w-]*\.[\w-]*\.[\w-]*$)"


@pytest_asyncio.fixture(scope="package")
async def steam_id() -> str:
    """steam_id ..."""
    return "1274105035093245124124"


@pytest_asyncio.fixture(scope="package")
async def jwt_token(steam_id: str) -> str:
    """Create a valid JWT token for test"""
    expires_in: timedelta = timedelta(minutes=5)
    payload   : dict[str, Any] = {
        "steamid": steam_id,
    }

    return await encode_jwt(
        expires_in=expires_in,
        payload=payload,
    )

@pytest_asyncio.fixture(scope="package")
async def jwt_token_exp() -> str:
    """Create an expired JWT token for test"""
    expires_in: timedelta = timedelta(minutes=5) - timedelta(minutes=10)

    return await encode_jwt(
        expires_in=expires_in,
        payload={},
    )
