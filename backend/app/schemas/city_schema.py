from pydantic import BaseModel


class CityResponse(BaseModel):
    id: int
    name: str
    country: str
    latitude: float | None = None
    longitude: float | None = None

