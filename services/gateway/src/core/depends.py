from dzshop.modules.database import UnitOfWork
from fastapi                 import Depends
from typing                  import Annotated

from adapters.database       import session
from core.requests           import HttpClient
from core.steam              import SteamService


def get_uow() -> UnitOfWork:
    """get_uow ..."""
    return UnitOfWork(session)


def get_http_client() -> HttpClient:
    """get_http_client ..."""
    return HttpClient()


unit_of_work : UnitOfWork   = Annotated[UnitOfWork, Depends(get_uow)]
http_client  : HttpClient   = Annotated[HttpClient, Depends(get_http_client)]
steam_service: SteamService = Annotated[SteamService, Depends(SteamService)]
