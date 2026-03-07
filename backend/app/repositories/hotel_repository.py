from sqlalchemy.orm import Session

from app.models.hotel import Hotel


def search_hotels(
    db: Session,
    city_id: int,
    min_price: float | None = None,
    max_price: float | None = None,
    rating: float | None = None,
    sort: str | None = None,
) -> list[Hotel]:
    query = db.query(Hotel).filter(Hotel.city_id == city_id)
    if min_price is not None:
        query = query.filter(Hotel.price_per_night >= min_price)
    if max_price is not None:
        query = query.filter(Hotel.price_per_night <= max_price)
    if rating is not None:
        query = query.filter(Hotel.rating >= rating)
    if sort == "price":
        query = query.order_by(Hotel.price_per_night.asc())
    elif sort == "rating":
        query = query.order_by(Hotel.rating.desc())
    return query.all()


def get_hotel_by_id(db: Session, hotel_id: int) -> Hotel | None:
    return db.query(Hotel).filter(Hotel.id == hotel_id).first()


def get_hotels_by_ids(db: Session, hotel_ids: list[int]) -> list[Hotel]:
    return db.query(Hotel).filter(Hotel.id.in_(hotel_ids)).all()
