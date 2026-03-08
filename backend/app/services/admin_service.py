from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.city import Attraction, City
from app.models.hotel import Hotel
from app.models.transport import TransportRoute
from app.schemas.admin_schema import (
    AttractionCreateRequest,
    AttractionUpdateRequest,
    CityCreateRequest,
    CityUpdateRequest,
    HotelCreateRequest,
    HotelUpdateRequest,
    TransportRouteCreateRequest,
    TransportRouteUpdateRequest,
)
from app.schemas.attraction_schema import AttractionResponse
from app.schemas.city_schema import CityResponse
from app.schemas.hotel_schema import HotelResponse
from app.schemas.transport_schema import TransportRouteResponse
from app.services.cache_service import delete_cached, make_key


# ── Helpers ───────────────────────────────────────────────────

def _invalidate_city_cache(city_id: int, search_bust: bool = True) -> None:
    delete_cached(make_key("cities", "id", city_id))
    if search_bust:
        # Bust wildcard search keys by deleting the known empty-string key (catches most autocomplete)
        delete_cached(make_key("cities", "search", ""))


def _invalidate_hotel_cache(hotel_id: int, city_id: int) -> None:
    delete_cached(make_key("hotels", "id", hotel_id))
    # Bust all search permutations for this city by deleting the base key
    delete_cached(make_key("hotels", "search", city_id, "", "", "", ""))
    delete_cached(make_key("hotels", "search", city_id, "", "", "", "price"))


def _invalidate_attraction_cache(attraction_id: int, city_id: int) -> None:
    delete_cached(make_key("attractions", "id", attraction_id))
    delete_cached(make_key("attractions", "city", city_id))


def _invalidate_route_cache(source_id: int, dest_id: int, route_id: int) -> None:
    delete_cached(make_key("routes", "id", route_id))
    delete_cached(make_key("routes", "search", source_id, dest_id, "any"))


# ── Cities ────────────────────────────────────────────────────

def create_city(db: Session, payload: CityCreateRequest) -> CityResponse:
    city = City(
        name=payload.name,
        country=payload.country,
        latitude=payload.latitude,
        longitude=payload.longitude,
        timezone=payload.timezone,
    )
    db.add(city)
    db.commit()
    db.refresh(city)
    delete_cached(make_key("cities", "search", ""))
    return CityResponse(id=city.id, name=city.name, country=city.country, latitude=city.latitude, longitude=city.longitude)


def update_city(db: Session, city_id: int, payload: CityUpdateRequest) -> CityResponse:
    city = db.query(City).filter(City.id == city_id).first()
    if not city:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found")
    for field, value in payload.model_dump(exclude_none=True).items():
        setattr(city, field, value)
    db.commit()
    db.refresh(city)
    _invalidate_city_cache(city_id)
    return CityResponse(id=city.id, name=city.name, country=city.country, latitude=city.latitude, longitude=city.longitude)


def delete_city(db: Session, city_id: int) -> None:
    city = db.query(City).filter(City.id == city_id).first()
    if not city:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found")
    _invalidate_city_cache(city_id)
    db.delete(city)
    db.commit()


# ── Hotels ────────────────────────────────────────────────────

def create_hotel(db: Session, payload: HotelCreateRequest) -> HotelResponse:
    hotel = Hotel(
        city_id=payload.city_id,
        name=payload.name,
        description=payload.description,
        latitude=payload.latitude,
        longitude=payload.longitude,
        rating=payload.rating,
        price_per_night=payload.price_per_night,
        total_rooms=payload.total_rooms,
        amenities=payload.amenities,
    )
    db.add(hotel)
    db.commit()
    db.refresh(hotel)
    _invalidate_hotel_cache(hotel.id, hotel.city_id)
    return HotelResponse(id=hotel.id, city_id=hotel.city_id, name=hotel.name, rating=hotel.rating or 0, price_per_night=hotel.price_per_night, latitude=hotel.latitude, longitude=hotel.longitude)


def update_hotel(db: Session, hotel_id: int, payload: HotelUpdateRequest) -> HotelResponse:
    hotel = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if not hotel:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hotel not found")
    for field, value in payload.model_dump(exclude_none=True).items():
        setattr(hotel, field, value)
    db.commit()
    db.refresh(hotel)
    _invalidate_hotel_cache(hotel_id, hotel.city_id)
    return HotelResponse(id=hotel.id, city_id=hotel.city_id, name=hotel.name, rating=hotel.rating or 0, price_per_night=hotel.price_per_night, latitude=hotel.latitude, longitude=hotel.longitude)


def delete_hotel(db: Session, hotel_id: int) -> None:
    hotel = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if not hotel:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hotel not found")
    _invalidate_hotel_cache(hotel_id, hotel.city_id)
    db.delete(hotel)
    db.commit()


# ── Attractions ───────────────────────────────────────────────

def create_attraction(db: Session, payload: AttractionCreateRequest) -> AttractionResponse:
    attraction = Attraction(
        city_id=payload.city_id,
        name=payload.name,
        category=payload.category,
        description=payload.description,
        latitude=payload.latitude,
        longitude=payload.longitude,
        rating=payload.rating,
        average_visit_time=payload.average_visit_time,
    )
    db.add(attraction)
    db.commit()
    db.refresh(attraction)
    _invalidate_attraction_cache(attraction.id, attraction.city_id)
    return AttractionResponse(id=attraction.id, city_id=attraction.city_id, name=attraction.name, category=attraction.category, rating=attraction.rating or 0, latitude=attraction.latitude, longitude=attraction.longitude)


def update_attraction(db: Session, attraction_id: int, payload: AttractionUpdateRequest) -> AttractionResponse:
    attraction = db.query(Attraction).filter(Attraction.id == attraction_id).first()
    if not attraction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attraction not found")
    for field, value in payload.model_dump(exclude_none=True).items():
        setattr(attraction, field, value)
    db.commit()
    db.refresh(attraction)
    _invalidate_attraction_cache(attraction_id, attraction.city_id)
    return AttractionResponse(id=attraction.id, city_id=attraction.city_id, name=attraction.name, category=attraction.category, rating=attraction.rating or 0, latitude=attraction.latitude, longitude=attraction.longitude)


def delete_attraction(db: Session, attraction_id: int) -> None:
    attraction = db.query(Attraction).filter(Attraction.id == attraction_id).first()
    if not attraction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attraction not found")
    _invalidate_attraction_cache(attraction_id, attraction.city_id)
    db.delete(attraction)
    db.commit()


# ── Transport Routes ──────────────────────────────────────────

def create_route(db: Session, payload: TransportRouteCreateRequest) -> TransportRouteResponse:
    from app.models.transport import TransportMode
    mode = db.query(TransportMode).filter(TransportMode.id == payload.transport_mode_id).first()
    if not mode:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transport mode not found")
    route = TransportRoute(
        source_city_id=payload.source_city_id,
        destination_city_id=payload.destination_city_id,
        transport_mode_id=payload.transport_mode_id,
        duration_minutes=payload.duration_minutes,
        distance_km=payload.distance_km,
        base_cost=payload.base_cost,
        stops=payload.stops,
    )
    db.add(route)
    db.commit()
    db.refresh(route)
    _invalidate_route_cache(route.source_city_id, route.destination_city_id, route.id)
    return TransportRouteResponse(route_id=route.id, mode=mode.name, duration=route.duration_minutes, cost=route.base_cost, stops=route.stops)


def update_route(db: Session, route_id: int, payload: TransportRouteUpdateRequest) -> TransportRouteResponse:
    from app.models.transport import TransportMode
    route = db.query(TransportRoute).filter(TransportRoute.id == route_id).first()
    if not route:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Route not found")
    for field, value in payload.model_dump(exclude_none=True).items():
        setattr(route, field, value)
    db.commit()
    db.refresh(route)
    _invalidate_route_cache(route.source_city_id, route.destination_city_id, route_id)
    mode = db.query(TransportMode).filter(TransportMode.id == route.transport_mode_id).first()
    return TransportRouteResponse(route_id=route.id, mode=mode.name if mode else "unknown", duration=route.duration_minutes, cost=route.base_cost, stops=route.stops)


def delete_route(db: Session, route_id: int) -> None:
    route = db.query(TransportRoute).filter(TransportRoute.id == route_id).first()
    if not route:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Route not found")
    _invalidate_route_cache(route.source_city_id, route.destination_city_id, route_id)
    db.delete(route)
    db.commit()
