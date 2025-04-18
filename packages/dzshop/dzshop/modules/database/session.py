from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, create_async_engine, async_sessionmaker
from collections.abc        import AsyncGenerator


def get_async_sessionmaker(database_url: str) -> async_sessionmaker[AsyncSession]:
    """Get async sessionmaker"""
    engine: AsyncEngine = create_async_engine(database_url)

    return async_sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )


async def get_db(database_url: str) -> AsyncGenerator[AsyncSession, None]:
    """Get async session"""
    session_maker = get_async_sessionmaker(database_url)

    async with session_maker() as session:
        try:
            yield session
        finally:
            await session.close()
