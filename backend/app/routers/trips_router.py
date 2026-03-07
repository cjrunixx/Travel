from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.repositories import trip_repository
from app.schemas.common import MessageResponse
from app.schemas.trip_schema import TripPlanRequest, TripPlanResponse
from app.services.planner_service import plan_trip
from app.utils.auth_utils import get_current_user_id
from app.repositories import city_repository, transport_repository, hotel_repository
from app.schemas.attraction_schema import AttractionResponse
from app.schemas.hotel_schema import HotelResponse
from app.schemas.transport_schema import TransportRouteResponse

router = APIRouter()


@router.post("/plan", response_model=TripPlanResponse)
def create_trip_plan(
    payload: TripPlanRequest,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
) -> TripPlanResponse:
    return plan_trip(db, payload, user_id)


@router.get("/{trip_id}", response_model=TripPlanResponse)
def get_trip_details(
    trip_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
) -> TripPlanResponse:
    trip = trip_repository.get_trip_by_id(db, trip_id)
    if not trip or trip.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trip not found")

    # Reconstruct cities
    source_city_obj = city_repository.get_city_by_id(db, trip.source_city_id)
    dest_city_obj = city_repository.get_city_by_id(db, trip.destination_city_id)
    
    if source_city_obj:
        source_city = CityResponse(
            id=source_city_obj.id, name=source_city_obj.name, country=source_city_obj.country,
            latitude=source_city_obj.latitude, longitude=source_city_obj.longitude
        )
    else:
        source_city = CityResponse(id=trip.source_city_id, name="Unknown", country="Unknown")
        
    if dest_city_obj:
        dest_city = CityResponse(
            id=dest_city_obj.id, name=dest_city_obj.name, country=dest_city_obj.country,
            latitude=dest_city_obj.latitude, longitude=dest_city_obj.longitude
        )
    else:
        dest_city = CityResponse(id=trip.destination_city_id, name="Unknown", country="Unknown")

    # Reconstruct transport
    trip_transports = trip_repository.get_trip_transport(db, trip_id)
    if trip_transports:
        result = transport_repository.get_route_by_id(db, trip_transports[0].route_id)
        if result:
            route_obj, mode_name = result
            transport = TransportRouteResponse(
                route_id=route_obj.id, mode=mode_name, duration=route_obj.duration_minutes,
                cost=route_obj.base_cost, stops=route_obj.stops,
            )
        else:
            transport = TransportRouteResponse(route_id=0, mode="none", duration=0, cost=0, stops=0)
    else:
        transport = TransportRouteResponse(route_id=0, mode="none", duration=0, cost=0, stops=0)

    # Reconstruct hotels
    trip_hotel_links = trip_repository.get_trip_hotels(db, trip_id)
    hotels = []
    hotel_ids = [th.hotel_id for th in trip_hotel_links]
    if hotel_ids:
        hotel_objs = hotel_repository.get_hotels_by_ids(db, hotel_ids)
        for h in hotel_objs:
            hotels.append(HotelResponse(
                id=h.id, city_id=h.city_id, name=h.name, rating=h.rating or 0, 
                price_per_night=h.price_per_night, latitude=h.latitude, longitude=h.longitude
            ))

    # Reconstruct attractions
    trip_attraction_links = trip_repository.get_trip_attractions(db, trip_id)
    attractions = []
    attraction_ids = [ta.attraction_id for ta in trip_attraction_links]
    if attraction_ids:
        attraction_objs = city_repository.get_attractions_by_ids(db, attraction_ids)
        for a in attraction_objs:
            attractions.append(AttractionResponse(
                id=a.id, city_id=a.city_id, name=a.name, category=a.category, 
                rating=a.rating or 0, latitude=a.latitude, longitude=a.longitude
            ))

    return TripPlanResponse(
        trip_id=trip.id,
        source_city=source_city,
        destination_city=dest_city,
        recommended_transport=transport,
        suggested_hotels=hotels,
        top_attractions=attractions,
    )



@router.post("/{trip_id}/save", response_model=MessageResponse)
def save_trip(
    trip_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
) -> MessageResponse:
    trip = trip_repository.get_trip_by_id(db, trip_id)
    if not trip or trip.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trip not found")
    return MessageResponse(message=f"Trip {trip_id} saved")


@router.post("/{trip_id}/attractions", response_model=MessageResponse)
def add_trip_attraction(
    trip_id: int,
    attraction_id: int = Query(...),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
) -> MessageResponse:
    trip = trip_repository.get_trip_by_id(db, trip_id)
    if not trip or trip.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trip not found")
    trip_repository.add_trip_attraction(db, trip_id, attraction_id)
    return MessageResponse(message=f"Attraction {attraction_id} added to trip {trip_id}")
