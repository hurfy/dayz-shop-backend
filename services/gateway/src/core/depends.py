from httpx      import AsyncClient

httpx_client: AsyncClient = AsyncClient()


async def get_httpx_client() -> AsyncClient:
    """Returns async httpx client"""
    return httpx_client
