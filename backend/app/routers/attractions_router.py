from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.schemas.attraction_schema import AttractionResponse
from app.services import city_service

router = APIRouter()


@router.get("", response_model=list[AttractionResponse])
def get_attractions(city_id: int = Query(...), db: Session = Depends(get_db)) -> list[AttractionResponse]:
    return city_service.get_attractions(db, city_id)


@router.get("/{attraction_id}", response_model=AttractionResponse)
def get_attraction_details(attraction_id: int, db: Session = Depends(get_db)) -> AttractionResponse:
    return city_service.get_attraction(db, attraction_id)
