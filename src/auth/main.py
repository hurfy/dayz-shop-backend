from shared.transport import service_router
from fastapi          import FastAPI

from app.transport    import auth_router


app: FastAPI = FastAPI()

app.include_router(auth_router)
app.include_router(service_router)
