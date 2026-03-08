from fastapi import APIRouter

from app.routers import (
    admin_router,
    advisories_router,
    attractions_router,
    auth_router,
    cities_router,
    hotels_router,
    transport_router,
    trips_router,
    users_router,
)

api_router = APIRouter()
api_router.include_router(auth_router.router, prefix="/auth", tags=["auth"])
api_router.include_router(users_router.router, prefix="/users", tags=["users"])
api_router.include_router(cities_router.router, prefix="/cities", tags=["cities"])
api_router.include_router(transport_router.router, prefix="/transport", tags=["transport"])
api_router.include_router(hotels_router.router, prefix="/hotels", tags=["hotels"])
api_router.include_router(attractions_router.router, prefix="/attractions", tags=["attractions"])
api_router.include_router(trips_router.router, prefix="/trips", tags=["trips"])
api_router.include_router(advisories_router.router, prefix="/advisories", tags=["advisories"])
api_router.include_router(admin_router.router, prefix="/admin", tags=["admin"])
