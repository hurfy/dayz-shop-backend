from fastapi.middleware.cors import CORSMiddleware
from contextlib              import asynccontextmanager
from fastapi                 import FastAPI

from shop.routers            import products_router
from database                import create_tables, delete_tables

origins = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "https://localhost:8000",
    "https://127.0.0.1:8000",
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_tables()
    await create_tables()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(products_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)