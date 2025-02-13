from typing import Any
from httpx  import AsyncClient, Response

SERVICES: dict[str, str] = {
    "auth"      : "http://auth_service:8001",
    "users"     : "http://users:8002",
    "items"     : "http://items:8003",
    "orders"    : "http://orders:8004",
    "categories": "http://categories:8005",
}


async def make_request(
        url: str, method: str, body: Any | None = None, headers: dict | None = None
) -> Response:
    """Sending http requests to internal modules"""
    async with AsyncClient() as client:
        return await client.request(
            url=url, method=method, json=body, headers=headers
        )
