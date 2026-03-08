from pydantic import BaseModel


# ── City ──────────────────────────────────────────────────────
class CityCreateRequest(BaseModel):
    name: str
    country: str
    latitude: float | None = None
    longitude: float | None = None
    timezone: str | None = None


class CityUpdateRequest(BaseModel):
    name: str | None = None
    country: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    timezone: str | None = None


# ── Hotel ─────────────────────────────────────────────────────
class HotelCreateRequest(BaseModel):
    city_id: int
    name: str
    description: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    rating: float | None = None
    price_per_night: float
    total_rooms: int | None = None
    amenities: str | None = None


class HotelUpdateRequest(BaseModel):
    name: str | None = None
    description: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    rating: float | None = None
    price_per_night: float | None = None
    total_rooms: int | None = None
    amenities: str | None = None


# ── Attraction ────────────────────────────────────────────────
class AttractionCreateRequest(BaseModel):
    city_id: int
    name: str
    category: str
    description: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    rating: float | None = None
    average_visit_time: int | None = None


class AttractionUpdateRequest(BaseModel):
    name: str | None = None
    category: str | None = None
    description: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    rating: float | None = None
    average_visit_time: int | None = None


# ── Transport Route ───────────────────────────────────────────
class TransportRouteCreateRequest(BaseModel):
    source_city_id: int
    destination_city_id: int
    transport_mode_id: int
    duration_minutes: int
    distance_km: float
    base_cost: float
    stops: int = 0


class TransportRouteUpdateRequest(BaseModel):
    duration_minutes: int | None = None
    distance_km: float | None = None
    base_cost: float | None = None
    stops: int | None = None
