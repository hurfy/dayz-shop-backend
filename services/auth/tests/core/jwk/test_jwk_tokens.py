import pytest

from typing          import Any

from core.jwk.tokens import create_jwk
from config          import auth_config


@pytest.mark.asyncio
async def test_create_jwk() -> None:
    """test_create_jwk ..."""
    jwk: dict[str, Any] = await create_jwk(auth_config.public_key)

    assert jwk is not None
    assert isinstance(jwk, dict)

    for field in {"kty", "alg", "use", "kid", "n", "e"}:
        assert field in jwk.keys()

        assert jwk[field] is not None
        assert isinstance(jwk[field], str)
