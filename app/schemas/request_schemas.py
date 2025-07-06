from pydantic import BaseModel


class ProductQuery(BaseModel):
    query: str  # e.g. "Where can I find milk?"
