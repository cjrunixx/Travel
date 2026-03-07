from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories import user_repository
from app.schemas.user_schema import UserPreferencesRequest, UserResponse


def get_profile(db: Session, user_id: int) -> UserResponse:
    user = user_repository.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserResponse(id=user.id, name=user.name, email=user.email)


def update_preferences(db: Session, user_id: int, payload: UserPreferencesRequest) -> None:
    user = user_repository.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user_repository.upsert_user_preferences(
        db,
        user_id=user_id,
        budget_preference=payload.budget_preference,
        travel_style=payload.travel_style,
        preferred_transport=payload.preferred_transport,
        alert_enabled=payload.alerts_enabled,
    )
