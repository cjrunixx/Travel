from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.schemas.auth_schema import AuthResponse, LoginRequest, RegisterRequest
from app.schemas.user_schema import UserResponse
from app.services import auth_service
from app.utils.auth_utils import get_current_user_id

router = APIRouter()


@router.post("/register", response_model=AuthResponse)
def register_user(payload: RegisterRequest, db: Session = Depends(get_db)) -> AuthResponse:
    return auth_service.register(db, payload)


@router.post("/login", response_model=AuthResponse)
def login_user(payload: LoginRequest, db: Session = Depends(get_db)) -> AuthResponse:
    return auth_service.login(db, payload)


@router.get("/me", response_model=UserResponse)
def get_me(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
) -> UserResponse:
    from app.services import user_service

    return user_service.get_profile(db, user_id)
