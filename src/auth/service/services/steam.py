from typing       import Any
from httpx        import AsyncClient, Response
from re           import search

from ..exceptions import SteamCheckError, InvalidSteamResponse
from ..schemas    import LoginRequest


class SteamService:
    def __init__(self, data: dict[str, Any]):
        self.url = self._generate_url(data)

    @staticmethod
    def _generate_url(data: dict[str, Any]) -> str:
        """Generates a link to check Steam auth"""
        base_url    : str = r"https://steamcommunity.com/openid/login?openid.mode=check_authentication"
        joined_query: str = "".join([f"&{k}={v}" for k, v in data.items()])

        return base_url + joined_query

    async def check_auth(self) -> bool:
        """Check authorization via OpenID in Steam"""
        async with AsyncClient() as client:
            response  : Response = await client.get(self.url)

            # Not success
            if not response.is_success:
                raise SteamCheckError("Failed to connect to Steam")

            # Not valid
            if not response.text.startswith("ns:"):
                raise InvalidSteamResponse("Invalid response from Steam")

            return search("is_valid:true", response.text) is not None


async def get_steam_service(data: LoginRequest) -> SteamService:
    """Get SteamService instance"""
    return SteamService(data.model_dump())