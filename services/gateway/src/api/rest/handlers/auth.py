from fastapi       import APIRouter, Depends, HTTPException, status
from typing        import Annotated
from httpx         import AsyncClient

from dzshop.errors import ServiceRequestError
from dzshop.enums  import RoleType
from dzshop.dto    import TokenPair, CreateToken
from core.steam    import SteamService
from config        import gateway_config

router: APIRouter = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=TokenPair,
)
async def login(
        ss: Annotated[SteamService, Depends(SteamService)]
) -> TokenPair:
    """login ..."""
    # Steam auth check failed
    if not await ss.check_auth():
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Steam authorization check failed")

    # Create tokens pair(auth service)
    async with AsyncClient() as client:
        data: CreateToken = CreateToken(
            steam_id=await ss.get_steam_id(),
            role=RoleType.admin,  # TODO: change
        )

        response = await client.post(
            url=gateway_config.auth_service_address,
            json=data.model_dump(mode="json"),
        )

        # Failed service request
        if not response.is_success:
            raise ServiceRequestError(
                status.HTTP_401_UNAUTHORIZED, detail="The request to auth service was not successful"
            )

    # ... create or update user in db

    return response.json()



# @router.post(
#     "/logout",
#     status_code=status.HTTP_200_OK,
#     response_model="",
# )
# async def logout() -> ...:
#     ...
#
#
# @router.post(
#     path="/logout-all",
#     status_code=status.HTTP_200_OK,
#     response_model="",
# )
# async def logout_all() -> ...:
#     ...
