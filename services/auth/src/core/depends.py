from fastapi                      import Depends
from typing                       import Annotated

from adapters.database.repository import IssuedTokensRepository

tokens_repository: IssuedTokensRepository = Annotated[IssuedTokensRepository, Depends(IssuedTokensRepository)]
