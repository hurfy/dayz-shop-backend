from dzshop.api import service_router
from fastapi    import FastAPI

from api.rest   import auth_router
from core.jwk   import create_jwk
from config     import auth_config

from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI) -> None:
    """FastAPI lifespan manager"""
    fastapi_app.state.jwk_cache = await create_jwk(auth_config.public_key)  # type: ignore[attr-defined]
    yield
    del fastapi_app.state.jwk_cache                                         # type: ignore[attr-defined]


app: FastAPI = FastAPI(
    lifespan=lifespan,
)

app.include_router(auth_router)
app.include_router(service_router)

