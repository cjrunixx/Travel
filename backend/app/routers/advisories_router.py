from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.schemas.advisory_schema import AdvisoryResponse
from app.services import advisory_service

router = APIRouter()


@router.get("", response_model=list[AdvisoryResponse])
def get_advisories(city_id: int = Query(...), db: Session = Depends(get_db)) -> list[AdvisoryResponse]:
    return advisory_service.get_advisories(db, city_id)
