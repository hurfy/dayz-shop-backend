from fastapi                      import Depends
from typing                       import Annotated

from adapters.database.repository import UsersRepository

users_repository: UsersRepository = Annotated[UsersRepository, Depends(UsersRepository)]
