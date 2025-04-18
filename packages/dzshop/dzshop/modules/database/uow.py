from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from types                  import TracebackType


class UnitOfWork:
    def __init__(self, session_maker: async_sessionmaker[AsyncSession]):
        self.session_maker = session_maker
        self.session: AsyncSession | None = None

    async def __aenter__(self) -> "UnitOfWork":
        self.session = self.session_maker()

        return self

    async def __aexit__(
            self,
            exc_type: BaseException | None,
            exc_val : BaseException | None,
            exc_tb  : TracebackType | None
    ) -> None:
        # Session not started
        if self.session is None:
            return

        try:
            if exc_type is not None:
                await self.rollback()
            else:
                await self.commit()

        finally:
            await self.close()

    async def commit(self) -> None:
        """Commit changes to the database"""
        if self.session is None:
            raise RuntimeError("Session not started")
        await self.session.commit()

    async def rollback(self) -> None:
        """Rollback changes to the database"""
        if self.session is None:
            raise RuntimeError("Session not started")
        await self.session.rollback()

    async def close(self) -> None:
        """Close the session"""
        if self.session is not None:
            await self.session.close()
            self.session = None
