from shared.dto import TokenPair
from fastapi    import APIRouter, Depends

from ...deps    import AClient, SSteam

router: APIRouter = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post(
    path="/login",
    dependencies=[Depends(AClient)],
    response_model=TokenPair,
)
async def login(client: AClient, ss: SSteam) -> TokenPair:
    return await client.post(
        url="http://auth:8001",
        json={"steam_id": ss.get_steam_id(), "role": "user"},
    )