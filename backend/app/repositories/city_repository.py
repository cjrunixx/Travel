from sqlalchemy.orm import Session

from app.models.city import Attraction, City


def search_cities(db: Session, search: str = "") -> list[City]:
    query = db.query(City)
    if search:
        query = query.filter(City.name.ilike(f"%{search}%"))
    return query.all()


def get_city_by_id(db: Session, city_id: int) -> City | None:
    return db.query(City).filter(City.id == city_id).first()


def get_attractions_by_city(db: Session, city_id: int) -> list[Attraction]:
    return db.query(Attraction).filter(Attraction.city_id == city_id).all()


def get_attraction_by_id(db: Session, attraction_id: int) -> Attraction | None:
    return db.query(Attraction).filter(Attraction.id == attraction_id).first()


def get_attractions_by_ids(db: Session, attraction_ids: list[int]) -> list[Attraction]:
    return db.query(Attraction).filter(Attraction.id.in_(attraction_ids)).all()
