from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm         import DeclarativeBase

from config                 import settings


db_engine   = create_async_engine(
    # SQLite
    # "sqlite+aiosqlite:///database.db"

    # PostgreSQL
    settings.DATABASE_URL_asyncpg
)
new_session = async_sessionmaker(
    db_engine, expire_on_commit=False
)


# Base model
class Model(DeclarativeBase):
    pass


async def create_tables() -> None:
    async with db_engine.begin() as connection:
        await connection.run_sync(Model.metadata.create_all)

async def delete_tables() -> None:
    async with db_engine.begin() as connection:
        await connection.run_sync(Model.metadata.drop_all)