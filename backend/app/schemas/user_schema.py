from pydantic import BaseModel, EmailStr


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr


class UserPreferencesRequest(BaseModel):
    budget_preference: str
    travel_style: str | None = None
    preferred_transport: str
    alerts_enabled: bool = True
