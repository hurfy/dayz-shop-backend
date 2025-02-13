from fastapi    import APIRouter, Depends, HTTPException, status
from typing     import Annotated

from ..errors   import SteamCheckError, SteamRequestError
from ..modules  import SteamService
from .responses import TokenPair

router: APIRouter = APIRouter()


@router.post(
    path="/create",
    status_code=status.HTTP_200_OK,
    response_model=TokenPair,
    dependencies=[Depends(SteamService)],
)
async def create(ss: Annotated[SteamService, Depends(SteamService)]) -> TokenPair:
    """create ..."""
    try:
        if not await ss.check_auth():
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Steam authorization check failed")

        ...  # Create jwt pair

    except (SteamRequestError, SteamCheckError) as e:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail=str(e)) from e


# @router.post(
#     path="/refresh",
#     status_code=status.HTTP_200_OK,
#     response_model=TokenPair,
# )
# async def refresh(data: RefreshResponse) -> TokenPair:
#     ...
