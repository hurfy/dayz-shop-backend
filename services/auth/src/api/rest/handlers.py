from dzshop.dto         import TokenPair
from fastapi            import APIRouter, Request, status

from api.rest.responses import JWKS
from api.rest.requests  import CreateToken, RefreshToken
from core.jwt           import create_access_token, create_refresh_token

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


@router.post(
    path="/refresh",
    status_code=status.HTTP_200_OK,
    response_model=TokenPair,
)
async def refresh(data: RefreshToken) -> TokenPair:
    """Refresh and creates a pair of access and refresh tokens"""
    ...


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
