from datetime import date

from sqlalchemy.orm import Session

from app.models.trip import Trip, TripAttraction, TripHotel, TripTransport


def create_trip(
    db: Session,
    user_id: int,
    source_city_id: int,
    destination_city_id: int,
    start_date: date,
    end_date: date,
    budget: float,
) -> Trip:
    trip = Trip(
        user_id=user_id,
        source_city_id=source_city_id,
        destination_city_id=destination_city_id,
        start_date=start_date,
        end_date=end_date,
        budget=budget,
    )
    db.add(trip)
    db.commit()
    db.refresh(trip)
    return trip


def get_trip_by_id(db: Session, trip_id: int) -> Trip | None:
    return db.query(Trip).filter(Trip.id == trip_id).first()


def get_trips_by_user(db: Session, user_id: int) -> list[Trip]:
    return db.query(Trip).filter(Trip.user_id == user_id).order_by(Trip.created_at.desc()).all()


def add_trip_transport(db: Session, trip_id: int, route_id: int, total_cost: float) -> TripTransport:
    tt = TripTransport(trip_id=trip_id, route_id=route_id, total_cost=total_cost)
    db.add(tt)
    db.commit()
    db.refresh(tt)
    return tt


def add_trip_hotel(
    db: Session, trip_id: int, hotel_id: int, checkin_date: date, checkout_date: date, total_cost: float
) -> TripHotel:
    th = TripHotel(
        trip_id=trip_id,
        hotel_id=hotel_id,
        checkin_date=checkin_date,
        checkout_date=checkout_date,
        total_cost=total_cost,
    )
    db.add(th)
    db.commit()
    db.refresh(th)
    return th


def add_trip_attraction(db: Session, trip_id: int, attraction_id: int, visit_date: date | None = None) -> TripAttraction:
    ta = TripAttraction(trip_id=trip_id, attraction_id=attraction_id, visit_date=visit_date)
    db.add(ta)
    db.commit()
    db.refresh(ta)
    return ta


def get_trip_transport(db: Session, trip_id: int) -> list[TripTransport]:
    return db.query(TripTransport).filter(TripTransport.trip_id == trip_id).all()


def get_trip_hotels(db: Session, trip_id: int) -> list[TripHotel]:
    return db.query(TripHotel).filter(TripHotel.trip_id == trip_id).all()


def get_trip_attractions(db: Session, trip_id: int) -> list[TripAttraction]:
    return db.query(TripAttraction).filter(TripAttraction.trip_id == trip_id).all()
