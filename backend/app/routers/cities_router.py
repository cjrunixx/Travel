from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.schemas.city_schema import CityResponse
from app.services import city_service

router = APIRouter()


@router.get("", response_model=list[CityResponse])
def search_cities(search: str = Query(default=""), db: Session = Depends(get_db)) -> list[CityResponse]:
    return city_service.search_cities(db, search)


@router.get("/{city_id}", response_model=CityResponse)
def get_city(city_id: int, db: Session = Depends(get_db)) -> CityResponse:
    return city_service.get_city(db, city_id)
