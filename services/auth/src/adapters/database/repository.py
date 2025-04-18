from dzshop.modules.database   import UnitOfWork
from typing                    import Any

from adapters.database.models  import IssuedToken
from adapters.database.session import session
from core.errors               import TokensPairWriteError


class IssuedTokensRepository:
    @classmethod
    async def create_tokens_pair(
            cls, access: dict[str, Any], refresh: dict[str, Any]
    ) -> None:
        """Create access token and refresh token in database"""
        async with UnitOfWork(session) as uow:
            try:
                access_token = IssuedToken(
                    jti=access["jti"],
                    subject=access["sub"],
                    type=access["type"],
                    expired=access["exp"]
                )

                refresh_token = IssuedToken(
                    jti=refresh["jti"],
                    subject=refresh["sub"],
                    type=refresh["type"],
                    expired=refresh["exp"]
                )

                uow.session.add_all([access_token, refresh_token])

            except Exception as exs:
                raise TokensPairWriteError() from exs
