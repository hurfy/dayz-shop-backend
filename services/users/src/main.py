from dzshop.api import service_router
from fastapi    import FastAPI

from api.rest   import users_router

app: FastAPI = FastAPI()

app.include_router(users_router)
app.include_router(service_router)
