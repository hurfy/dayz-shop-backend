from fastapi import HTTPException, status
from typing  import Optional
from httpx   import AsyncClient, Response, HTTPStatusError, RequestError


class HttpClient:
    _instance: Optional["HttpClient"] = None

    def __new__(cls) -> "HttpClient":
        """singleton ..."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._client = AsyncClient()

        return cls._instance

    async def get(self, url: str, **kwargs) -> Response:
        """get ..."""
        return await self._request("GET", url, **kwargs)

    async def post(self, url: str, **kwargs) -> Response:
        """post ..."""
        return await self._request("POST", url, **kwargs)

    async def put(self, url: str, **kwargs) -> Response:
        """put ..."""
        return await self._request("PUT", url, **kwargs)

    async def delete(self, url: str, **kwargs) -> Response:
        """delete ..."""
        return await self._request("DELETE", url, **kwargs)

    async def patch(self, url: str, **kwargs) -> Response:
        """patch ..."""
        return await self._request("PATCH", url, **kwargs)

    async def head(self, url: str, **kwargs) -> Response:
        """head ..."""
        return await self._request("HEAD", url, **kwargs)

    async def options(self, url: str, **kwargs) -> Response:
        """options ..."""
        return await self._request("OPTIONS", url, **kwargs)

    async def aclose(self):
        """aclose ..."""
        await self._client.aclose()

    async def _request(self, method: str, url: str, **kwargs) -> Response:
        """Executes the request. Handles negative responses and network errors"""
        try:
            response = await self._client.request(method, url, **kwargs)
            response.raise_for_status()

            return response

        except HTTPStatusError as exs:
            raise HTTPException(
                status_code=exs.response.status_code, detail=exs.response.text
            ) from exs

        except RequestError as exs:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=f"Service: {url}({exs})"
            ) from exs
