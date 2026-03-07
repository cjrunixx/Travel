from sqlalchemy.orm import Session

from app.repositories import advisory_repository
from app.schemas.advisory_schema import AdvisoryResponse


def get_advisories(db: Session, city_id: int) -> list[AdvisoryResponse]:
    advisories = advisory_repository.get_advisories_by_city(db, city_id)
    return [
        AdvisoryResponse(id=a.id, city_id=a.city_id, category=a.category, severity=a.severity, title=a.title)
        for a in advisories
    ]
