from dzshop.dto   import SteamUserDTO
from fastapi      import APIRouter, Response, HTTPException, status

from core.depends import users_repository
from core.errors  import UserWriteError

router: APIRouter = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.put(
    path="/upsert",
    status_code=status.HTTP_200_OK,
    response_model=None,
)
async def upsert_user(
        data: SteamUserDTO, ur: users_repository,
) -> Response:
    """Create or update user"""
    try:
        result: bool = await ur.create_or_update(
            data=data,
        )

        return Response(
            status_code=status.HTTP_201_CREATED if result else status.HTTP_204_NO_CONTENT
        )

    # Database error
    except UserWriteError as exs:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exs),
        ) from exs
