from pydantic import BaseModel


class HotelResponse(BaseModel):
    id: int
    city_id: int
    name: str
    rating: float
    price_per_night: float
    latitude: float | None = None
    longitude: float | None = None

