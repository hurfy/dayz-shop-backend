from redis import Redis, from_url

DEFAULT_URL: str = "redis://localhost:6379"

class RedisClient:
    _instance: Redis | None = None

    @classmethod
    async def get_instance(cls, url: str = DEFAULT_URL) -> Redis:
        """Get Redis singleton-instance with connection pool"""
        if cls._instance is None:
            cls._instance = await from_url(
                url,
                encoding="utf-8",
                decode_responses=True,
                max_connections=10,
            )

        return cls._instance

    @classmethod
    async def close(cls):
        """Close Redis connection"""
        if cls._instance:
            await cls._instance.close()
            cls._instance = None


async def get_redis(url: str = DEFAULT_URL) -> Redis:
    """Get Redis singleton-instance"""
    return await RedisClient.get_instance(url)
