from pydantic import BaseModel


class LocationResponse(BaseModel):
    product: str
    aisle: str


class ComboResponse(BaseModel):
    suggestions: list[str]
