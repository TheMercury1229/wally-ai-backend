from fastapi import APIRouter
from app.schemas.request_schemas import ComboQuery
from app.schemas.response_schemas import ComboResponse
from app.services.combo_handler import suggest_combos

router = APIRouter()


@router.post("/recommend", response_model=ComboResponse)
def combo_recommendation(data: ComboQuery):
    results = suggest_combos(data.purpose)
    return {"suggestions": results}
