from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.schemas.common import MessageResponse
from app.schemas.user_schema import UserPreferencesRequest, UserResponse
from app.services import user_service

router = APIRouter()


@router.get("/{user_id}", response_model=UserResponse)
def get_user_profile(user_id: int, db: Session = Depends(get_db)) -> UserResponse:
    return user_service.get_profile(db, user_id)


@router.put("/{user_id}/preferences", response_model=MessageResponse)
def update_preferences(user_id: int, payload: UserPreferencesRequest, db: Session = Depends(get_db)) -> MessageResponse:
    user_service.update_preferences(db, user_id, payload)
    return MessageResponse(message=f"Preferences updated for user {user_id}")
