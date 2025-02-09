from fastapi.middleware.cors import CORSMiddleware
from contextlib              import asynccontextmanager
from fastapi                 import FastAPI

from database                import create_tables, delete_tables
from api                     import products_crud_router, categories_crud_router, orders_crud_router, orders_router

origins = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "https://localhost:8000",
    "https://127.0.0.1:8000",
]


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """lifespan ..."""
    await delete_tables()
    await create_tables()
    yield


app = FastAPI(
    lifespan=lifespan,
    title="DayZ Exsidium Shop",
    version="0.1",
    contact={
        "name" : "hurfy",
        "url"  : "https://t.me/thehurfy",
        "email": "hurfydev+dayzshop@gmail.com",
    },
    license_info={
        "name": "MIT License",
        "url" : "https://github.com/hurfy/dayz-shop-backend/blob/main/LICENSE",
    },
)

app.include_router(products_crud_router)
app.include_router(categories_crud_router)
app.include_router(orders_crud_router)
app.include_router(orders_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
