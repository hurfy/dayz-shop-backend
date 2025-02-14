from httpx     import AsyncClient

from ...errors import SteamCheckError, SteamRequestError
from ...dto    import SteamLogin


class SteamService:
    url: str = r"https://steamcommunity.com/openid/login"

    def __init__(self, params: SteamLogin) -> None:
        self.params = params.model_dump(mode="json", check=True)

    async def check_auth(self) -> bool:
        """Check authorization status for security purposes"""
        async with AsyncClient() as client:
            response = await client.get(
                url=self.url, params=self.params
            )

            if not response.is_success:
                raise SteamRequestError(response.status_code, response.text)

            return await self._parse_status(response.text)

    async def get_steam_id(self) -> str:
        """Get steam id from claimed id url"""
        return self.params["openid.claimed_id"].split("/")[-1]

    async def _parse_status(self, text: str) -> bool:
        """Parse the response from Steam"""
        # Something obviously went wrong
        if fr"ns:{self.params['openid.ns']}" not in text:
            raise SteamCheckError()

        return "is_valid:true" in text
