from dzshop.api    import service_router
from contextlib    import asynccontextmanager
from fastapi       import FastAPI

from core.requests import HttpClient
from core.jwk      import decode_jwk
from api.rest      import auth_router


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI) -> None:
    """FastAPI lifespan manager"""
    fastapi_app.state.jwk_cache = await decode_jwk() # type: ignore[attr-defined]

    yield

    await HttpClient().aclose()
    del fastapi_app.state.jwk_cache  # type: ignore[attr-defined]


app: FastAPI = FastAPI(
    lifespan=lifespan,
)

app.include_router(auth_router)
app.include_router(service_router)
