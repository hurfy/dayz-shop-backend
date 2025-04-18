import pytest

from unittest.mock           import AsyncMock

from dzshop.modules.database import UnitOfWork


@pytest.mark.asyncio
async def test_uow_commit(uow: UnitOfWork, async_session: AsyncMock) -> None:
    """Check that commit is called on closing"""
    # Exiting the context itself will call commit()
    async with uow:
        pass

    async_session.commit.assert_awaited_once()
    async_session.close.assert_awaited_once()


@pytest.mark.asyncio
async def test_uow_rollback_on_exception(uow: UnitOfWork, async_session: AsyncMock) -> None:
    """Check that rollback is called when an error occurs"""
    with pytest.raises(ValueError):
        async with uow:
            raise ValueError("Test error")

    async_session.rollback.assert_awaited_once()
    async_session.close.assert_awaited_once()


@pytest.mark.asyncio
async def test_uow_no_session_no_commit(uow: UnitOfWork) -> None:
    """Check that commit is not called if a session has not been created"""
    with pytest.raises(RuntimeError, match="Session not started"):
        await uow.commit()


@pytest.mark.asyncio
async def test_uow_no_session_no_rollback(uow: UnitOfWork) -> None:
    """Verify that rollback is not called if a session has not been created"""
    with pytest.raises(RuntimeError, match="Session not started"):
        await uow.rollback()


@pytest.mark.asyncio
async def test_uow_close_closes_session(uow: UnitOfWork, async_session: AsyncMock) -> None:
    """Check that the session is closed"""
    async with uow:
        await uow.close()

    async_session.close.assert_awaited_once()
