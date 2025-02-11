from fastapi     import APIRouter, Depends, HTTPException, status

from .exceptions import InvalidSteamResponse, SteamCheckError
from .services   import SteamService, get_steam_service
from .schemas    import RefreshResponse, TokenResponse, LoginRequest

router: APIRouter = APIRouter()


@router.post(
    path="/create",
    status_code=status.HTTP_200_OK,
    response_model=TokenResponse,
    dependencies=[Depends(get_steam_service)],
)
async def create(ss: SteamService = Depends(get_steam_service)) -> TokenResponse:
    try:
        if not await ss.check_auth():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Steam authorization check failed",
            )

        # Get tokens
        ...

        return TokenResponse(access_token="", refresh_token="")

    # Steam check auth errors
    except (InvalidSteamResponse, SteamCheckError) as exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Failed to authenticate: {exception}",
        ) from exception


# @router.post(
#     path="/refresh",
#     status_code=status.HTTP_200_OK,
#     response_model=TokenResponse,
# )
# async def refresh(data: RefreshResponse) -> TokenResponse:
#     ...