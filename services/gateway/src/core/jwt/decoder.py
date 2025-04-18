from fastapi import Request
from typing  import Any
from jwt     import decode


async def decode_jwt(
        token    : str | bytes,
        request: Request,
        algorithm: str = "RS256"
) -> dict[str, Any]:
    """decode_jwt ..."""
    return decode(
        token,
        request.app.state.jwk_cache,
        algorithms=[algorithm],
    )
