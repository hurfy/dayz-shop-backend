from fastapi import FastAPI
from service.routers import router

# Create an app with disabling doc, cause it's a gateway
app = FastAPI(docs_url=None, redoc_url=None)
app.include_router(router)
