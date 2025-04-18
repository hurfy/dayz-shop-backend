from dzshop.modules.database import get_async_sessionmaker
from sqlalchemy.ext.asyncio  import AsyncSession, async_sessionmaker

from config                  import auth_config

session: async_sessionmaker[AsyncSession] = get_async_sessionmaker(
    auth_config.database_address
)
