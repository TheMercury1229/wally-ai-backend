from typing import List
from pydantic import BaseModel


class ProductQuery(BaseModel):
    query: str  # e.g. "Where can I find milk?"


class ComboQuery(BaseModel):
    purpose: str  # e.g., "birthday party"


class PastOrder(BaseModel):
    product_name: str
    price: float
    category: str
    timestamp: str  # ISO format string


class SurpriseMeRequest(BaseModel):
    user_id: str
    history: List[PastOrder]
