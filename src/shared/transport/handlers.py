from fastapi    import APIRouter, status

from .responses import HealthCheck

router: APIRouter = APIRouter(
    prefix="/service",
    tags=["service"],
)


@router.get(
    path="/health",
    response_model=HealthCheck,
    status_code=status.HTTP_200_OK,
)
async def health_check() -> HealthCheck:
    """Check service status"""
    return HealthCheck()
