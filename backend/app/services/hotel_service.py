from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories import hotel_repository
from app.schemas.hotel_schema import HotelResponse


def search_hotels(
    db: Session,
    city_id: int,
    min_price: float | None = None,
    max_price: float | None = None,
    rating: float | None = None,
    sort: str | None = None,
) -> list[HotelResponse]:
    hotels = hotel_repository.search_hotels(db, city_id, min_price, max_price, rating, sort)
    return [
        HotelResponse(id=h.id, city_id=h.city_id, name=h.name, rating=h.rating or 0, price_per_night=h.price_per_night)
        for h in hotels
    ]


def get_hotel(db: Session, hotel_id: int) -> HotelResponse:
    h = hotel_repository.get_hotel_by_id(db, hotel_id)
    if not h:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hotel not found")
    return HotelResponse(id=h.id, city_id=h.city_id, name=h.name, rating=h.rating or 0, price_per_night=h.price_per_night)
