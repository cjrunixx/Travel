from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories import transport_repository
from app.schemas.transport_schema import TransportRouteResponse


def search_routes(
    db: Session,
    source_city_id: int,
    destination_city_id: int,
    transport_mode: str | None = None,
) -> list[TransportRouteResponse]:
    results = transport_repository.search_routes(db, source_city_id, destination_city_id, transport_mode)
    return [
        TransportRouteResponse(
            route_id=route.id,
            mode=mode_name,
            duration=route.duration_minutes,
            cost=route.base_cost,
            stops=route.stops,
        )
        for route, mode_name in results
    ]


def get_route(db: Session, route_id: int) -> TransportRouteResponse:
    result = transport_repository.get_route_by_id(db, route_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Route not found")
    route, mode_name = result
    return TransportRouteResponse(
        route_id=route.id,
        mode=mode_name,
        duration=route.duration_minutes,
        cost=route.base_cost,
        stops=route.stops,
    )
