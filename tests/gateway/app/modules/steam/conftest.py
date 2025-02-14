import pytest_asyncio

from gateway.app.modules import SteamService
from gateway.app.dto     import SteamLogin


@pytest_asyncio.fixture(scope="package")
async def steam_login() -> SteamLogin:
    """steam_login ..."""
    return SteamLogin(
        ns="http://specs.openid.net/auth/2.0",
        mode="id_res",
        op_endpoint="https://steamcommunity.com/openid/login",
        claimed_id="https://steamcommunity.com/openid/id/76561199223994494",
        identity="https://steamcommunity.com/openid/id/76561199223994494",
        return_to="http://127.0.0.1:8000/auth/callback",
        response_nonce="2025-02-11T09:33:36ZqrkzhSnePkWVvpzrwmrw9q4l8kU=",
        assoc_handle="1234567890",
        signed="signed,op_endpoint,claimed_id,identity,return_to,response_nonce,assoc_handle",
        sig="ucMcHFsL76VKu6YEHbAHVIy3m9k=",
    )


@pytest_asyncio.fixture(scope="package")
async def steam_service(steam_login: SteamLogin) -> SteamService:
    """Create SteamService instance"""
    return SteamService(steam_login)


@pytest_asyncio.fixture(scope="package")
async def steam_id_re_pattern() -> str:
    """steam_id_re_pattern ..."""
    return r"^\d+$"
