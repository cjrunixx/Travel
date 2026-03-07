from pydantic import BaseModel


class AttractionResponse(BaseModel):
    id: int
    city_id: int
    name: str
    category: str
    rating: float
    latitude: float | None = None
    longitude: float | None = None

