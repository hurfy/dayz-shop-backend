from dzshop.modules.database import UnitOfWork
from fastapi                 import Depends
from typing                  import Annotated

from adapters.database       import UsersRepository, session


async def get_uow() -> UnitOfWork:
    """uow ..."""
    return UnitOfWork(session)


unit_of_work    : UnitOfWork      = Annotated[UnitOfWork, Depends(get_uow)]
users_repository: UsersRepository = Annotated[UsersRepository, Depends(UsersRepository)]
