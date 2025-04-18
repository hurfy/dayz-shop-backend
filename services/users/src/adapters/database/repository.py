from dzshop.modules.database   import UnitOfWork
from dzshop.dto                import SteamUserDTO
from sqlalchemy                import select

from core.errors               import UserWriteError

from adapters.database.session import session
from adapters.database.models  import User


class UsersRepository:
    @classmethod
    async def create_or_update(cls, data: SteamUserDTO) -> bool:
        """Create new user or update existing one"""
        is_new: bool = False

        async with UnitOfWork(session) as uow:
            try:
                user: User | None = await uow.session.scalar(
                    select(User).where(User.steam_id == data.steam_id)
                )

                if user:
                    # Update user
                    for field, value in data.model_dump(exclude_unset=True, mode="json").items():
                        setattr(user, field, value)
                else:
                    # Create user
                    user = User(**data.model_dump(mode="json"))
                    uow.session.add(user)

                    is_new = True

                return is_new

            except Exception as exs:
                raise UserWriteError("update" if user else "create", exs) from exs
