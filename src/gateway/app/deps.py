from fastapi  import Depends
from typing   import Annotated
from httpx    import AsyncClient

from .modules import SteamService, get_httpx_client


AClient: AsyncClient  = Annotated[AsyncClient, Depends(get_httpx_client)]
SSteam : SteamService = Annotated[SteamService, Depends(SteamService)]
