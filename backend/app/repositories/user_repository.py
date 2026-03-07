from sqlalchemy.orm import Session

from app.models.user import User, UserPreference


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def create_user(db: Session, name: str, email: str, password_hash: str) -> User:
    user = User(name=name, email=email, password_hash=password_hash)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_preferences(db: Session, user_id: int) -> UserPreference | None:
    return db.query(UserPreference).filter(UserPreference.user_id == user_id).first()


def upsert_user_preferences(
    db: Session,
    user_id: int,
    budget_preference: str,
    travel_style: str | None,
    preferred_transport: str,
    alert_enabled: bool,
) -> UserPreference:
    pref = get_user_preferences(db, user_id)
    if pref is None:
        pref = UserPreference(
            user_id=user_id,
            budget_preference=budget_preference,
            travel_style=travel_style,
            preferred_transport=preferred_transport,
            alert_enabled=alert_enabled,
        )
        db.add(pref)
    else:
        pref.budget_preference = budget_preference
        pref.travel_style = travel_style
        pref.preferred_transport = preferred_transport
        pref.alert_enabled = alert_enabled
    db.commit()
    db.refresh(pref)
    return pref
