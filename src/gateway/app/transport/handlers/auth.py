from shared.dto import TokenPair
from fastapi    import APIRouter, Depends

from ...modules import SteamService, get_httpx_client
from ...deps    import AClient, SSteam

router: APIRouter = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post(
    path="/login",
    dependencies=[Depends(SteamService), Depends(get_httpx_client)],
    response_model=TokenPair,
)
async def login(ss: SSteam, client: AClient) -> TokenPair:
    """login ..."""
    response = await client.post(
        url="http://shop-auth:8001/auth/create",
        json={"steam_id": await ss.get_steam_id(), "role": "user"},
    )

    return TokenPair(**response.json())
