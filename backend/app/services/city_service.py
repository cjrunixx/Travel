from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories import city_repository
from app.schemas.attraction_schema import AttractionResponse
from app.schemas.city_schema import CityResponse
from app.services.cache_service import CITY_TTL, get_cached, make_key, set_cached


def search_cities(db: Session, search: str = "") -> list[CityResponse]:
    key = make_key("cities", "search", search.lower().strip())
    cached = get_cached(key)
    if cached is not None:
        return [CityResponse(**c) for c in cached]

    cities = city_repository.search_cities(db, search)
    result = [CityResponse(id=c.id, name=c.name, country=c.country, latitude=c.latitude, longitude=c.longitude) for c in cities]
    set_cached(key, [r.model_dump() for r in result], ttl=CITY_TTL)
    return result


def get_city(db: Session, city_id: int) -> CityResponse:
    key = make_key("cities", "id", city_id)
    cached = get_cached(key)
    if cached is not None:
        return CityResponse(**cached)

    city = city_repository.get_city_by_id(db, city_id)
    if not city:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found")
    result = CityResponse(id=city.id, name=city.name, country=city.country, latitude=city.latitude, longitude=city.longitude)
    set_cached(key, result.model_dump(), ttl=CITY_TTL)
    return result


def get_attractions(db: Session, city_id: int) -> list[AttractionResponse]:
    key = make_key("attractions", "city", city_id)
    cached = get_cached(key)
    if cached is not None:
        return [AttractionResponse(**a) for a in cached]

    attractions = city_repository.get_attractions_by_city(db, city_id)
    result = [
        AttractionResponse(id=a.id, city_id=a.city_id, name=a.name, category=a.category, rating=a.rating or 0, latitude=a.latitude, longitude=a.longitude)
        for a in attractions
    ]
    set_cached(key, [r.model_dump() for r in result], ttl=CITY_TTL)
    return result


def get_attraction(db: Session, attraction_id: int) -> AttractionResponse:
    key = make_key("attractions", "id", attraction_id)
    cached = get_cached(key)
    if cached is not None:
        return AttractionResponse(**cached)

    a = city_repository.get_attraction_by_id(db, attraction_id)
    if not a:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attraction not found")
    result = AttractionResponse(id=a.id, city_id=a.city_id, name=a.name, category=a.category, rating=a.rating or 0, latitude=a.latitude, longitude=a.longitude)
    set_cached(key, result.model_dump(), ttl=CITY_TTL)
    return result
