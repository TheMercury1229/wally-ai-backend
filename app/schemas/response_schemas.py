from pydantic import BaseModel


class LocationResponse(BaseModel):
    product: str
    aisle: str


class ComboResponse(BaseModel):
    suggestions: list[str]


class ImageSearchResponse(BaseModel):
    found: bool
    message: str


class SurpriseMeResponse(BaseModel):
    suggestion: str  # e.g., "Protein Bar"
    message: str     # e.g., "Craving a treat? Grab a choco-almond bar near Aisle 4!"
