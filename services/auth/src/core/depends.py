from dzshop.modules.database import UnitOfWork
from fastapi                 import Depends
from typing                  import Annotated

from adapters.database       import session


async def uow() -> UnitOfWork:
    """uow ..."""
    return UnitOfWork(session)


unit_of_work: UnitOfWork = Annotated[UnitOfWork, Depends(uow)]
