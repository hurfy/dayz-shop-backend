import pytest

from unittest.mock        import AsyncMock
from redis                import Redis

from dzshop.modules.redis import RedisClient, get_redis


@pytest.mark.asyncio
async def test_get_instance_creates_new_instance(mocker: AsyncMock) -> None:
    """test_get_instance_creates_new_instance ..."""
    mock_redis    = mocker.AsyncMock(spec=Redis)
    mock_from_url = mocker.patch(
        "dzshop.modules.redis.client.from_url", new_callable=mocker.AsyncMock, return_value=mock_redis
    )

    # Make sure the instance is created
    instance_one = await RedisClient.get_instance()
    assert instance_one == mock_redis
    mock_from_url.assert_called_once()

    # Make sure that the callback doesn't call from_url again
    instance_two = await RedisClient.get_instance()
    assert instance_two is instance_one
    mock_from_url.assert_called_once()


@pytest.mark.asyncio
async def test_close_resets_instance(mocker: AsyncMock) -> None:
    """test_close_resets_instance ..."""
    mock_redis = mocker.AsyncMock(spec=Redis)
    RedisClient._instance = mock_redis

    mock_redis.close = mocker.AsyncMock()

    await RedisClient.close()

    mock_redis.close.assert_awaited_once()
    assert RedisClient._instance is None


@pytest.mark.asyncio
async def test_get_redis_calls_get_instance(mocker: AsyncMock) -> None:
    """test_get_redis_calls_get_instance ..."""
    mock_instance     = mocker.AsyncMock(spec=Redis)
    mock_get_instance = mocker.patch.object(
        RedisClient, "get_instance", return_value=mock_instance
    )

    redis: Redis = await get_redis()

    assert redis == mock_instance
    mock_get_instance.assert_awaited_once()
