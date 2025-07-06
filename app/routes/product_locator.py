from fastapi import APIRouter
from app.schemas.request_schemas import ProductQuery
from app.schemas.response_schemas import LocationResponse
from app.services.llm_handler import locate_product

router = APIRouter()


@router.post("/locate", response_model=LocationResponse)
def locate_item(data: ProductQuery):
    result = locate_product(data.query)
    return {
        "product": data.query,
        "aisle": result["response"]
    }
