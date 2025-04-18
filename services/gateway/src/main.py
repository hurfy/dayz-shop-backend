from dzshop.api    import service_router
from contextlib    import asynccontextmanager
from fastapi       import FastAPI

from core.requests import HttpClient
from api.rest      import auth_router


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI) -> None:
    """FastAPI lifespan manager"""
    yield
    await HttpClient().aclose()


app: FastAPI = FastAPI(
    lifespan=lifespan,
)

app.include_router(auth_router)
app.include_router(service_router)
