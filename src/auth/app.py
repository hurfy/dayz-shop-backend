from fastapi import FastAPI

from service import auth_router

app: FastAPI = FastAPI()
app.include_router(auth_router)
