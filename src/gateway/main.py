from contextlib    import asynccontextmanager
from fastapi       import FastAPI

from app.transport import auth_router
from app.modules   import httpx_client


@asynccontextmanager
async def lifespan(app: FastAPI) -> None: # noqa
    """lifespan ..."""
    ...
    yield
    await httpx_client.aclose()


app: FastAPI = FastAPI(lifespan=lifespan)
app.include_router(auth_router)
