from dzshop.dto        import TokenPair
from fastapi           import APIRouter, status

from api.rest.requests import CreateToken
from core.jwt          import create_access_token, create_refresh_token

router: APIRouter = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post(
    path="/create",
    status_code=status.HTTP_200_OK,
    response_model=TokenPair,
)
async def create(data: CreateToken) -> TokenPair:
    """Creates a pair of access and refresh tokens"""
    access_token : str = await create_access_token(data.steam_id, data.role)
    refresh_token: str = await create_refresh_token(data.steam_id, data.role)

    # ... save to db(for revoke)

    return TokenPair(
        access_token=access_token,
        refresh_token=refresh_token,
    )

    # try:
    #     if not await ss.check_auth():
    #         raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Steam authorization check failed")
    #
    #     steam_id: str = ss.get_steam_id()
    #
    #     access_token : str = create_access_token(data.steam_id)
    #     refresh_token: str = create_refresh_token(data.steam_id)
    #
    #     # ... save to db(for revoke)
    #
    #     return TokenPair(
    #         access_token=access_token,
    #         refresh_token=refresh_token,
    #     )
    #
    # except (SteamRequestError, SteamCheckError) as e:
    #     raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail=str(e)) from e


# @router.post(
#     path="/refresh",
#     status_code=status.HTTP_200_OK,
#     response_model=TokenPair,
# )
# async def refresh(data: RefreshResponse) -> TokenPair:
#     ...
