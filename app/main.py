from fastapi import FastAPI
from app.routes import product_locator
from app.routes import combo_recommender
app = FastAPI()

app.include_router(product_locator.router, prefix="/api/v1", tags=["Locator"])
app.include_router(combo_recommender.router,
                   prefix="/api/v1", tags=["Recommendations"])
