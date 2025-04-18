from fastapi           import Depends
from typing            import Annotated

from adapters.database import IssuedTokensRepository

tokens_repository: IssuedTokensRepository = Annotated[IssuedTokensRepository, Depends(IssuedTokensRepository)]
