from fastapi import FastAPI

from service import gateway_router

# Create an app with disabling doc, cause it's a gateway
app: FastAPI = FastAPI(docs_url=None, redoc_url=None)
app.include_router(gateway_router)
