from fastapi import APIRouter
from app.schemas.request_schemas import SurpriseMeRequest
from app.schemas.response_schemas import SurpriseMeResponse
from app.services.surprise_me import generate_surprise_product

router = APIRouter()


@router.post("/surprise-me", response_model=SurpriseMeResponse)
def surprise_me(req: SurpriseMeRequest):
    result = generate_surprise_product(
        req.user_id, [order.dict() for order in req.history])
    return result
