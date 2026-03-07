from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories import user_repository
from app.schemas.auth_schema import AuthResponse, LoginRequest, RegisterRequest
from app.utils.auth_utils import create_access_token, hash_password, verify_password


def register(db: Session, payload: RegisterRequest) -> AuthResponse:
    existing = user_repository.get_user_by_email(db, payload.email)
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    hashed = hash_password(payload.password)
    user = user_repository.create_user(db, name=payload.name, email=payload.email, password_hash=hashed)
    token = create_access_token(subject=str(user.id))
    return AuthResponse(access_token=token, user_id=user.id)


def login(db: Session, payload: LoginRequest) -> AuthResponse:
    user = user_repository.get_user_by_email(db, payload.email)
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token(subject=str(user.id))
    return AuthResponse(access_token=token, user_id=user.id)
