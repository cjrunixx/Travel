from sqlalchemy.orm import Session

from app.models.advisory import Advisory


def get_advisories_by_city(db: Session, city_id: int) -> list[Advisory]:
    return db.query(Advisory).filter(Advisory.city_id == city_id).all()
