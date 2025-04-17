from sqlalchemy.ext.asyncio  import AsyncSession, async_sessionmaker

from dzshop.modules.database import get_async_sessionmaker
from config                  import users_config

session: async_sessionmaker[AsyncSession] = get_async_sessionmaker(
    users_config.database_address
)
