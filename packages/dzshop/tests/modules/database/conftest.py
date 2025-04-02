import pytest_asyncio

from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, async_sessionmaker
from unittest.mock          import AsyncMock, MagicMock

from modules.database       import UnitOfWork


@pytest_asyncio.fixture(scope="function")
def async_session(mocker: AsyncMock) -> AsyncMock:
    """async_session ..."""
    return mocker.AsyncMock(spec=AsyncSession)


@pytest_asyncio.fixture(scope="function")
def async_engine(mocker: AsyncMock) -> AsyncMock:
    """async_engine ..."""
    engine = mocker.AsyncMock(spec=AsyncEngine)
    engine.dispose = mocker.AsyncMock()

    return engine


@pytest_asyncio.fixture(scope="function")
def sessionmaker(mocker: AsyncMock, async_session: AsyncMock) -> MagicMock:
    """sessionmaker ..."""
    maker = mocker.MagicMock(spec=async_sessionmaker)
    maker.return_value = async_session

    return maker


@pytest_asyncio.fixture(scope="function")
async def uow(sessionmaker: MagicMock) -> UnitOfWork:
    """uow ..."""
    return UnitOfWork(sessionmaker)



@pytest_asyncio.fixture(scope="package")
async def database_url() -> str:
    """database_url ..."""
    return "postgresql+asyncpg://user:pass@localhost/db"
