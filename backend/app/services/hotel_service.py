from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories import hotel_repository
from app.schemas.hotel_schema import HotelResponse
from app.services.cache_service import HOTEL_TTL, get_cached, make_key, set_cached


def search_hotels(
    db: Session,
    city_id: int,
    min_price: float | None = None,
    max_price: float | None = None,
    rating: float | None = None,
    sort: str | None = None,
) -> list[HotelResponse]:
    key = make_key("hotels", "search", city_id, min_price or "", max_price or "", rating or "", sort or "")
    cached = get_cached(key)
    if cached is not None:
        return [HotelResponse(**h) for h in cached]

    hotels = hotel_repository.search_hotels(db, city_id, min_price, max_price, rating, sort)
    result = [
        HotelResponse(id=h.id, city_id=h.city_id, name=h.name, rating=h.rating or 0, price_per_night=h.price_per_night, latitude=h.latitude, longitude=h.longitude)
        for h in hotels
    ]
    set_cached(key, [r.model_dump() for r in result], ttl=HOTEL_TTL)
    return result


def get_hotel(db: Session, hotel_id: int) -> HotelResponse:
    key = make_key("hotels", "id", hotel_id)
    cached = get_cached(key)
    if cached is not None:
        return HotelResponse(**cached)

    h = hotel_repository.get_hotel_by_id(db, hotel_id)
    if not h:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hotel not found")
    result = HotelResponse(id=h.id, city_id=h.city_id, name=h.name, rating=h.rating or 0, price_per_night=h.price_per_night, latitude=h.latitude, longitude=h.longitude)
    set_cached(key, result.model_dump(), ttl=HOTEL_TTL)
    return result
