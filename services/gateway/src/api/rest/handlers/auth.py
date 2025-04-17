from dzshop.enums import RoleType
from dzshop.dto   import TokenPairDTO, CreateTokenDTO, SteamUserDTO
from fastapi      import APIRouter, HTTPException, status
from httpx        import Response

from core.depends import http_client, steam_service
from core.errors  import EmptySteamPlayersError, SteamCheckError
from config       import gateway_config

router: APIRouter = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post(
    path="/login",
    status_code=status.HTTP_200_OK,
    response_model=TokenPairDTO,
)
async def login(
        ss: steam_service, hc: http_client,
) -> TokenPairDTO:
    """login ..."""
    try:
        # Check Steam auth(SteamAPI)
        if await ss.check_auth():  # TODO: add "not"
            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED, detail="Steam authorization check failed"
            )

        # Fetch user data(SteamAPI)
        user_data: SteamUserDTO = await ss.get_user_data()

    except (SteamCheckError, EmptySteamPlayersError) as exs:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail=str(exs)) from exs

    # Create or update user in database(Users)
    await hc.put(
        url=gateway_config.users_service_address + "/upsert",
        json=user_data.model_dump(mode="json", by_alias=True),
    )

    # Prepare token creation request
    data: CreateTokenDTO = CreateTokenDTO(
        steam_id=await ss.get_steam_id(),
        role=RoleType.admin,  # TODO: make dynamic
    )

    # Create tokens pair(Auth)
    response: Response = await hc.post(
        url=gateway_config.auth_service_address + "/create",
        json=data.model_dump(mode="json"),
    )

    return TokenPairDTO.model_validate(
        response.json()
    )


# @router.post(
#     path="/logout",
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
