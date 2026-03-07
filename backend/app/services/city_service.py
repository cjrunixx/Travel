from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories import city_repository
from app.schemas.attraction_schema import AttractionResponse
from app.schemas.city_schema import CityResponse


def search_cities(db: Session, search: str = "") -> list[CityResponse]:
    cities = city_repository.search_cities(db, search)
    return [CityResponse(id=c.id, name=c.name, country=c.country) for c in cities]


def get_city(db: Session, city_id: int) -> CityResponse:
    city = city_repository.get_city_by_id(db, city_id)
    if not city:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found")
    return CityResponse(id=city.id, name=city.name, country=city.country)


def get_attractions(db: Session, city_id: int) -> list[AttractionResponse]:
    attractions = city_repository.get_attractions_by_city(db, city_id)
    return [
        AttractionResponse(id=a.id, city_id=a.city_id, name=a.name, category=a.category, rating=a.rating or 0)
        for a in attractions
    ]


def get_attraction(db: Session, attraction_id: int) -> AttractionResponse:
    a = city_repository.get_attraction_by_id(db, attraction_id)
    if not a:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attraction not found")
    return AttractionResponse(id=a.id, city_id=a.city_id, name=a.name, category=a.category, rating=a.rating or 0)
