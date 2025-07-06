from pydantic import BaseModel


class ProductQuery(BaseModel):
    query: str  # e.g. "Where can I find milk?"


class ComboQuery(BaseModel):
    purpose: str  # e.g., "birthday party"
