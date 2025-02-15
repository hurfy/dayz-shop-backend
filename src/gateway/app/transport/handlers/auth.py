from shared.dto import TokenPair
from fastapi    import APIRouter, Depends, HTTPException, status
from httpx      import Response

from ...modules import SteamService, get_httpx_client
from ...errors  import SteamRequestError, SteamCheckError
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
    """Checks authorization in steam and gives access tokens (creates or changes user in the database)"""
    # Try to check auth on the steam side
    try:
        if not await ss.check_auth():
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Steam authorization check failed")

    except (SteamRequestError, SteamCheckError) as error:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED) from error


    tokens: Response = await client.post(
        url="http://shop-auth:8001/auth/create",
        json={"steam_id": await ss.get_steam_id(), "role": "user"},
    )

    return TokenPair(**tokens.json())
