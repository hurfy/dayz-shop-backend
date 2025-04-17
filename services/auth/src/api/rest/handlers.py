from dzshop.dto         import TokenPairDTO, CreateTokenDTO
from datetime           import datetime
from fastapi            import APIRouter, Request, status
from typing             import Any

from api.rest.responses import JwksDTO
from api.rest.requests  import RefreshTokenDTO
from adapters.database  import IssuedToken
from core.depends       import unit_of_work
from core.jwt           import create_access_token, create_refresh_token, decode_jwt

router: APIRouter = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post(
    path="/create",
    status_code=status.HTTP_200_OK,
    response_model=TokenPairDTO,
)
async def create(data: CreateTokenDTO, uow: unit_of_work, request: Request) -> TokenPairDTO:
    """Creates a pair of access and refresh tokens"""
    access_token : str = await create_access_token(data.steam_id, data.role)
    refresh_token: str = await create_refresh_token(data.steam_id, data.role)

    # omg cringe :/
    # TODO: rework tokens system ...
    decoded: dict[str, Any] = await decode_jwt(refresh_token)

    # TODO: move to repository layer ...
    async with uow:
        uow.session.add(
            IssuedToken(
                jti=decoded["jti"],
                expired=datetime.fromtimestamp(decoded["exp"]),
                subject=data.steam_id,
                # device_id=decoded["did"],
            )
        )

    return TokenPairDTO(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.post(
    path="/refresh",
    status_code=status.HTTP_200_OK,
    response_model=TokenPairDTO,
)
async def refresh(data: RefreshTokenDTO) -> TokenPairDTO:
    """Refresh and creates a pair of access and refresh tokens"""
    ...
    # ... check if type is refresh
    # ... check if exists in db


@router.get(
    path="/.well-known/jwks.json",
    status_code=status.HTTP_200_OK,
    response_model=JwksDTO,
)
async def get_jwks(request: Request) -> JwksDTO:
    """Returns a list of JWK tokens"""
    return JwksDTO(
        keys=[request.app.state.jwk_cache,]
    )
