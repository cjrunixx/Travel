from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.schemas.hotel_schema import HotelResponse
from app.services import hotel_service

router = APIRouter()


@router.get("", response_model=list[HotelResponse])
def search_hotels(
    city_id: int = Query(...),
    min_price: float | None = Query(default=None),
    max_price: float | None = Query(default=None),
    rating: float | None = Query(default=None),
    sort: str | None = Query(default=None),
    db: Session = Depends(get_db),
) -> list[HotelResponse]:
    return hotel_service.search_hotels(db, city_id, min_price, max_price, rating, sort)


@router.get("/{hotel_id}", response_model=HotelResponse)
def get_hotel_details(hotel_id: int, db: Session = Depends(get_db)) -> HotelResponse:
    return hotel_service.get_hotel(db, hotel_id)
