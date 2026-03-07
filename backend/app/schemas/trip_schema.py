from pydantic import BaseModel

from app.schemas.attraction_schema import AttractionResponse
from app.schemas.city_schema import CityResponse
from app.schemas.hotel_schema import HotelResponse
from app.schemas.transport_schema import TransportRouteResponse


class TripPlanRequest(BaseModel):
    source_city_id: int
    destination_city_id: int
    start_date: str
    end_date: str
    budget: float


class TripPlanResponse(BaseModel):
    trip_id: int
    source_city: CityResponse
    destination_city: CityResponse
    recommended_transport: TransportRouteResponse
    suggested_hotels: list[HotelResponse]
    top_attractions: list[AttractionResponse]
