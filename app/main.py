from fastapi import FastAPI
from app.routes import product_locator, combo_recommender, image_search, surprise_me

app = FastAPI()

app.include_router(product_locator.router, prefix="/api/v1", tags=["Locator"])
app.include_router(combo_recommender.router,
                   prefix="/api/v1", tags=["Recommendations"])
app.include_router(image_search.router, prefix="/api/v1",
                   tags=["Vision Search"])
app.include_router(surprise_me.router, prefix="/api/v1", tags=["Surprise"])
