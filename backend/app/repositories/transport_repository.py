from sqlalchemy.orm import Session

from app.models.transport import TransportMode, TransportRoute


def search_routes(
    db: Session,
    source_city_id: int,
    destination_city_id: int,
    transport_mode: str | None = None,
) -> list[tuple[TransportRoute, str]]:
    """Return list of (route, mode_name) tuples."""
    query = (
        db.query(TransportRoute, TransportMode.name)
        .join(TransportMode, TransportRoute.transport_mode_id == TransportMode.id)
        .filter(
            TransportRoute.source_city_id == source_city_id,
            TransportRoute.destination_city_id == destination_city_id,
        )
    )
    if transport_mode:
        query = query.filter(TransportMode.name == transport_mode)
    return query.all()


def get_route_by_id(db: Session, route_id: int) -> tuple[TransportRoute, str] | None:
    result = (
        db.query(TransportRoute, TransportMode.name)
        .join(TransportMode, TransportRoute.transport_mode_id == TransportMode.id)
        .filter(TransportRoute.id == route_id)
        .first()
    )
    return result


def get_cheapest_route(
    db: Session, source_city_id: int, destination_city_id: int
) -> tuple[TransportRoute, str] | None:
    result = (
        db.query(TransportRoute, TransportMode.name)
        .join(TransportMode, TransportRoute.transport_mode_id == TransportMode.id)
        .filter(
            TransportRoute.source_city_id == source_city_id,
            TransportRoute.destination_city_id == destination_city_id,
        )
        .order_by(TransportRoute.base_cost.asc())
        .first()
    )
    return result
