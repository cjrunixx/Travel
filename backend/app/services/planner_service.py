from datetime import date

from sqlalchemy.orm import Session

from app.repositories import city_repository, hotel_repository, transport_repository, trip_repository
from app.schemas.attraction_schema import AttractionResponse
from app.schemas.city_schema import CityResponse
from app.schemas.hotel_schema import HotelResponse
from app.schemas.transport_schema import TransportRouteResponse
from app.schemas.trip_schema import TripPlanRequest, TripPlanResponse


def plan_trip(db: Session, payload: TripPlanRequest, user_id: int) -> TripPlanResponse:
    # Fetch city details
    source_city_obj = city_repository.get_city_by_id(db, payload.source_city_id)
    dest_city_obj = city_repository.get_city_by_id(db, payload.destination_city_id)

    if not source_city_obj or not dest_city_obj:
        # Fallback or error handling
        source_city = CityResponse(id=payload.source_city_id, name="Unknown", country="Unknown")
        dest_city = CityResponse(id=payload.destination_city_id, name="Unknown", country="Unknown")
    else:
        source_city = CityResponse(
            id=source_city_obj.id, name=source_city_obj.name, country=source_city_obj.country,
            latitude=source_city_obj.latitude, longitude=source_city_obj.longitude
        )
        dest_city = CityResponse(
            id=dest_city_obj.id, name=dest_city_obj.name, country=dest_city_obj.country,
            latitude=dest_city_obj.latitude, longitude=dest_city_obj.longitude
        )

    # Fetch cheapest route
    route_result = transport_repository.get_cheapest_route(db, payload.source_city_id, payload.destination_city_id)
    if route_result:
        route_obj, mode_name = route_result
        route = TransportRouteResponse(
            route_id=route_obj.id,
            mode=mode_name,
            duration=route_obj.duration_minutes,
            cost=route_obj.base_cost,
            stops=route_obj.stops,
        )
    else:
        route = TransportRouteResponse(route_id=0, mode="none", duration=0, cost=0, stops=0)

    # Fetch hotels within budget, sorted by price
    max_hotel_budget = payload.budget * 0.5  # allocate up to 50% of budget for hotel
    hotel_objs = hotel_repository.search_hotels(
        db, payload.destination_city_id, max_price=max_hotel_budget, sort="price"
    )
    hotels = [
        HotelResponse(
            id=h.id, city_id=h.city_id, name=h.name, rating=h.rating or 0,
            price_per_night=h.price_per_night, latitude=h.latitude, longitude=h.longitude
        )
        for h in hotel_objs[:5]
    ]

    # Fetch top attractions in destination city
    attraction_objs = city_repository.get_attractions_by_city(db, payload.destination_city_id)
    top_attraction_objs = sorted(attraction_objs, key=lambda a: a.rating or 0, reverse=True)[:5]
    attractions = [
        AttractionResponse(
            id=a.id, city_id=a.city_id, name=a.name, category=a.category,
            rating=a.rating or 0, latitude=a.latitude, longitude=a.longitude
        )
        for a in top_attraction_objs
    ]

    # Persist trip record
    trip_start_date = date.fromisoformat(payload.start_date)
    trip_end_date = date.fromisoformat(payload.end_date)
    trip = trip_repository.create_trip(
        db,
        user_id=user_id,
        source_city_id=payload.source_city_id,
        destination_city_id=payload.destination_city_id,
        start_date=trip_start_date,
        end_date=trip_end_date,
        budget=payload.budget,
    )

    # Save selected transport
    if route_result:
        trip_repository.add_trip_transport(db, trip.id, route_obj.id, route_obj.base_cost)

    # Save suggested hotels
    top_hotel_objs = hotel_objs[:5]
    for h in top_hotel_objs:
        trip_repository.add_trip_hotel(db, trip.id, h.id, trip_start_date, trip_end_date, h.price_per_night)

    # Save top attractions
    for a in top_attraction_objs:
        trip_repository.add_trip_attraction(db, trip.id, a.id)

    return TripPlanResponse(
        trip_id=trip.id,
        source_city=source_city,
        destination_city=dest_city,
        recommended_transport=route,
        suggested_hotels=hotels,
        top_attractions=attractions,
    )

