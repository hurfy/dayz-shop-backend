from dzshop.dto.jwks import JwksDTO
from httpx           import Response

from core.requests   import HttpClient
from config          import gateway_config


async def fetch_jwks() -> JwksDTO:
    """Fetch JWKS from auth service"""
    response: Response = await HttpClient().get(
        url=gateway_config.auth_service_address + "/.well-known/jwks.json"
    )

    return JwksDTO(**response.json())
