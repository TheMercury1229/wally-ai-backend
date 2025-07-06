from fastapi import FastAPI
from app.routes import product_locator

app = FastAPI()

app.include_router(product_locator.router, prefix="/api/v1", tags=["Locator"])
