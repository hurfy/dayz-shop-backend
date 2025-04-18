from fastapi       import Depends
from typing        import Annotated

from core.requests import HttpClient
from core.steam    import SteamService


def get_http_client() -> HttpClient:
    """get_http_client ..."""
    return HttpClient()


http_client  : HttpClient   = Annotated[HttpClient, Depends(get_http_client)]
steam_service: SteamService = Annotated[SteamService, Depends(SteamService)]
