from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.config.database import get_db
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
from app.schemas.common import MessageResponse
from app.schemas.hotel_schema import HotelResponse
from app.schemas.transport_schema import TransportRouteResponse
from app.services import admin_service
from app.utils.auth_utils import require_admin

router = APIRouter()


# ── Cities ────────────────────────────────────────────────────

@router.post("/cities", response_model=CityResponse, status_code=status.HTTP_201_CREATED)
def create_city(
    payload: CityCreateRequest,
    db: Session = Depends(get_db),
    _: int = Depends(require_admin),
) -> CityResponse:
    return admin_service.create_city(db, payload)


@router.put("/cities/{city_id}", response_model=CityResponse)
def update_city(
    city_id: int,
    payload: CityUpdateRequest,
    db: Session = Depends(get_db),
    _: int = Depends(require_admin),
) -> CityResponse:
    return admin_service.update_city(db, city_id, payload)


@router.delete("/cities/{city_id}", response_model=MessageResponse)
def delete_city(
    city_id: int,
    db: Session = Depends(get_db),
    _: int = Depends(require_admin),
) -> MessageResponse:
    admin_service.delete_city(db, city_id)
    return MessageResponse(message=f"City {city_id} deleted")


# ── Hotels ────────────────────────────────────────────────────

@router.post("/hotels", response_model=HotelResponse, status_code=status.HTTP_201_CREATED)
def create_hotel(
    payload: HotelCreateRequest,
    db: Session = Depends(get_db),
    _: int = Depends(require_admin),
) -> HotelResponse:
    return admin_service.create_hotel(db, payload)


@router.put("/hotels/{hotel_id}", response_model=HotelResponse)
def update_hotel(
    hotel_id: int,
    payload: HotelUpdateRequest,
    db: Session = Depends(get_db),
    _: int = Depends(require_admin),
) -> HotelResponse:
    return admin_service.update_hotel(db, hotel_id, payload)


@router.delete("/hotels/{hotel_id}", response_model=MessageResponse)
def delete_hotel(
    hotel_id: int,
    db: Session = Depends(get_db),
    _: int = Depends(require_admin),
) -> MessageResponse:
    admin_service.delete_hotel(db, hotel_id)
    return MessageResponse(message=f"Hotel {hotel_id} deleted")


# ── Attractions ───────────────────────────────────────────────

@router.post("/attractions", response_model=AttractionResponse, status_code=status.HTTP_201_CREATED)
def create_attraction(
    payload: AttractionCreateRequest,
    db: Session = Depends(get_db),
    _: int = Depends(require_admin),
) -> AttractionResponse:
    return admin_service.create_attraction(db, payload)


@router.put("/attractions/{attraction_id}", response_model=AttractionResponse)
def update_attraction(
    attraction_id: int,
    payload: AttractionUpdateRequest,
    db: Session = Depends(get_db),
    _: int = Depends(require_admin),
) -> AttractionResponse:
    return admin_service.update_attraction(db, attraction_id, payload)


@router.delete("/attractions/{attraction_id}", response_model=MessageResponse)
def delete_attraction(
    attraction_id: int,
    db: Session = Depends(get_db),
    _: int = Depends(require_admin),
) -> MessageResponse:
    admin_service.delete_attraction(db, attraction_id)
    return MessageResponse(message=f"Attraction {attraction_id} deleted")


# ── Transport Routes ──────────────────────────────────────────

@router.post("/transport/routes", response_model=TransportRouteResponse, status_code=status.HTTP_201_CREATED)
def create_route(
    payload: TransportRouteCreateRequest,
    db: Session = Depends(get_db),
    _: int = Depends(require_admin),
) -> TransportRouteResponse:
    return admin_service.create_route(db, payload)


@router.put("/transport/routes/{route_id}", response_model=TransportRouteResponse)
def update_route(
    route_id: int,
    payload: TransportRouteUpdateRequest,
    db: Session = Depends(get_db),
    _: int = Depends(require_admin),
) -> TransportRouteResponse:
    return admin_service.update_route(db, route_id, payload)


@router.delete("/transport/routes/{route_id}", response_model=MessageResponse)
def delete_route(
    route_id: int,
    db: Session = Depends(get_db),
    _: int = Depends(require_admin),
) -> MessageResponse:
    admin_service.delete_route(db, route_id)
    return MessageResponse(message=f"Route {route_id} deleted")
