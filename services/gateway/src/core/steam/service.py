from dzshop.dto.steam import SteamLoginDTO, SteamUserDTO
from typing           import Any
from httpx            import Response

from core.requests    import HttpClient
from core.errors      import SteamCheckError, EmptySteamPlayersError
from config           import gateway_config


class SteamService:
    openid_url   : str = r"https://steamcommunity.com/openid/login"
    steam_api_url: str = r"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/"  # noqa (http)

    def __init__(self, params: SteamLoginDTO) -> None:
        self._params: dict[str, Any] = params.model_dump(mode="json", check=True)
        self._client: HttpClient     = HttpClient()

    def get_params(self) -> SteamLoginDTO:
        """SteamLogin getter"""
        return self._params

    async def check_auth(self) -> bool:
        """Check authorization status for security purposes"""
        response: Response = await self._client.get(
            url=self.openid_url,
            params=self._params,
        )

        return await self._parse_status(response.text)

    async def get_user_data(self) -> SteamUserDTO:
        """Fetch user data"""
        params: dict[str, Any] = {
            "key": gateway_config.steam_api_key,
            "steamids": await self.get_steam_id(),
        }

        response: Response = await self._client.get(
            url=self.steam_api_url,
            params=params,
        )

        json_data: dict[str, Any]       = response.json()
        players  : list[dict[str, Any]] = json_data.get("response", {}).get("players", [])

        if not players:
            raise EmptySteamPlayersError()

        return SteamUserDTO.model_validate(players[0])

    async def get_steam_id(self) -> str:
        """Get steam id from claimed id url"""
        return self._params["openid.claimed_id"].split("/")[-1]

    async def _parse_status(self, text: str) -> bool:
        """Parse the response from Steam"""
        if fr"ns:{self._params['openid.ns']}" not in text:
            raise SteamCheckError()

        return "is_valid:true" in text
