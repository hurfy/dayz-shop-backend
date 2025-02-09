from fastapi.responses import JSONResponse
from fastapi           import APIRouter, HTTPException, Request
from typing            import Any

from .services         import SERVICES, make_request

router = APIRouter()


@router.api_route(
    path="/{service}/{path:path}",
    methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
)
async def gateway(service: str, path: str, request: Request) -> JSONResponse:
    """gateway ..."""
    # Not found(Invalid service)
    if service not in SERVICES:
        raise HTTPException(status_code=404, detail="Service not found")

    has_body: bool = request.method in ("POST", "PUT", "PATCH")

    # Collecting query data
    service_url: str = SERVICES[service]
    headers    : dict = dict(request.headers)
    body       : Any | None = await request.json() if has_body else None

    response = await make_request(f"{service_url}/{path}", request.method, body, headers)

    return JSONResponse(
        status_code=response.status_code, content=response.json()
    )
