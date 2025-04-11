from dzshop.dto              import TokenPair, CreateToken
from fastapi                 import APIRouter, Request, status
from typing                  import Any

from api.rest.responses      import JWKS
from api.rest.requests       import RefreshToken
from adapters.database       import IssuedToken
from core.depends            import UOW
from core.jwt                import create_access_token, create_refresh_token, decode_jwt

router: APIRouter = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post(
    path="/create",
    status_code=status.HTTP_200_OK,
    response_model=TokenPair,
)
async def create(data: CreateToken, uow: UOW, request: Request) -> TokenPair:
    """Creates a pair of access and refresh tokens"""
    print(request.headers.get("X-Device-ID"))

    access_token : str = await create_access_token(data.steam_id, data.role)
    refresh_token: str = await create_refresh_token(data.steam_id, data.role)

    # omg cringe :/
    decoded: dict[str, Any] = await decode_jwt(refresh_token)

    async with uow:
        uow.session.add(
            IssuedToken(
                jti=decoded["jti"],
                subject=data.steam_id,
                # device_id=decoded["did"],
            )
        )

    return TokenPair(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.post(
    path="/refresh",
    status_code=status.HTTP_200_OK,
    response_model=TokenPair,
)
async def refresh(data: RefreshToken) -> TokenPair:
    """Refresh and creates a pair of access and refresh tokens"""
    ...
    # ... check if type is refresh
    # ... check if exists in db


@router.get(
    path="/.well-known/jwks.json",
    status_code=status.HTTP_200_OK,
    response_model=JWKS,
)
async def get_jwks(request: Request) -> JWKS:
    """Returns a list of JWK tokens"""
    return JWKS(
        keys=[request.app.state.jwk_cache,]
    )
