from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.schemas.transport_schema import TransportRouteResponse
from app.services import transport_service

router = APIRouter()


@router.get("/routes", response_model=list[TransportRouteResponse])
def get_routes(
    source_city_id: int = Query(...),
    destination_city_id: int = Query(...),
    date: str | None = Query(default=None),
    transport_mode: str | None = Query(default=None),
    db: Session = Depends(get_db),
) -> list[TransportRouteResponse]:
    return transport_service.search_routes(db, source_city_id, destination_city_id, transport_mode)


@router.get("/routes/{route_id}", response_model=TransportRouteResponse)
def get_route_details(route_id: int, db: Session = Depends(get_db)) -> TransportRouteResponse:
    return transport_service.get_route(db, route_id)
