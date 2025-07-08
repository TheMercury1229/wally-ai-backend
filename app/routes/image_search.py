from fastapi import APIRouter, UploadFile, File
from app.services.image_query import image_to_product_location
from app.schemas.response_schemas import ImageSearchResponse
import os
router = APIRouter()


@router.post("/image-search", response_model=ImageSearchResponse)
async def search_by_image(file: UploadFile = File(...)):
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(await file.read())

    result = image_to_product_location(temp_path)
    # Clean up the temporary file if necessary
    if os.path.exists(temp_path):
        os.remove(temp_path)
    return result
