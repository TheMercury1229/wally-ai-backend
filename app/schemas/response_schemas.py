from pydantic import BaseModel


class LocationResponse(BaseModel):
    product: str
    aisle: str
