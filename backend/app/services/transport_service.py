from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories import transport_repository
from app.schemas.transport_schema import TransportRouteResponse
from app.services.cache_service import TRANSPORT_TTL, get_cached, make_key, set_cached


def search_routes(
    db: Session,
    source_city_id: int,
    destination_city_id: int,
    transport_mode: str | None = None,
) -> list[TransportRouteResponse]:
    key = make_key("routes", "search", source_city_id, destination_city_id, transport_mode or "any")
    cached = get_cached(key)
    if cached is not None:
        return [TransportRouteResponse(**r) for r in cached]

    results = transport_repository.search_routes(db, source_city_id, destination_city_id, transport_mode)
    result = [
        TransportRouteResponse(
            route_id=route.id,
            mode=mode_name,
            duration=route.duration_minutes,
            cost=route.base_cost,
            stops=route.stops,
        )
        for route, mode_name in results
    ]
    set_cached(key, [r.model_dump() for r in result], ttl=TRANSPORT_TTL)
    return result


def get_route(db: Session, route_id: int) -> TransportRouteResponse:
    key = make_key("routes", "id", route_id)
    cached = get_cached(key)
    if cached is not None:
        return TransportRouteResponse(**cached)

    result = transport_repository.get_route_by_id(db, route_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Route not found")
    route, mode_name = result
    response = TransportRouteResponse(
        route_id=route.id,
        mode=mode_name,
        duration=route.duration_minutes,
        cost=route.base_cost,
        stops=route.stops,
    )
    set_cached(key, response.model_dump(), ttl=TRANSPORT_TTL)
    return response
