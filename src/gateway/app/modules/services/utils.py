from fastapi import Depends
from typing  import Annotated
from httpx   import AsyncClient


async def get_httpx_client() -> AsyncClient:
    """Returns async httpx client"""
    async with AsyncClient() as client:
        return client



