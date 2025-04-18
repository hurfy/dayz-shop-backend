from dzshop.dto         import TokenPairDTO, CreateTokenDTO
from fastapi            import APIRouter, Request, status, HTTPException

from api.rest.responses import JwksDTO
from api.rest.requests  import RefreshTokenDTO
from core.depends       import tokens_repository
from core.errors        import TokensPairWriteError
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
async def create(data: CreateTokenDTO, tr: tokens_repository, request: Request) -> TokenPairDTO:
    """Creates a pair of access and refresh tokens"""
    access_token : str = await create_access_token(data.steam_id, data.role)
    refresh_token: str = await create_refresh_token(data.steam_id, data.role)

    # omg cringe :/
    # TODO: rework tokens system ...
    try:
        tr.create_tokens_pair(
            access_token=await decode_jwt(access_token),
            refresh_token=await decode_jwt(refresh_token),
        )

    except TokensPairWriteError as exs:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exs)) from exs

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
