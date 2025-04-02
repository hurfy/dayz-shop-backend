import pytest

from sqlalchemy.ext.asyncio   import async_sessionmaker
from unittest.mock            import AsyncMock, MagicMock

from modules.database.session import get_async_sessionmaker, get_db


@pytest.mark.asyncio
async def test_get_async_sessionmaker(
        mocker: AsyncMock, database_url: str, async_engine: AsyncMock
) -> None:
    """Test that get_async_sessionmaker creates a sessionmaker with the right engine"""
    mock_create_engine = mocker.patch(
        "modules.database.session.create_async_engine",
        return_value=async_engine
    )

    session_maker = get_async_sessionmaker(database_url)

    assert isinstance(session_maker, async_sessionmaker)
    mock_create_engine.assert_called_once_with(database_url)


@pytest.mark.asyncio
async def test_get_db(
        mocker: AsyncMock, database_url: str, sessionmaker: MagicMock, async_session: AsyncMock
) -> None:
    """Test that get_db creates a session and closes it correctly"""
    mocker.patch(
        "modules.database.session.get_async_sessionmaker",
        return_value=sessionmaker
    )

    # Configure __aenter__() to return the desired mock-session
    sessionmaker.return_value.__aenter__.return_value = async_session

    async def consume():
        async for session in get_db(database_url):
            assert session is async_session

    await consume()
