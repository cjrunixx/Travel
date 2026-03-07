from app.models.advisory import Advisory
from app.models.city import Attraction, City
from app.models.hotel import Hotel
from app.models.transport import TransportMode, TransportRoute
from app.models.trip import Trip, TripAttraction, TripHotel, TripTransport
from app.models.user import User, UserPreference

__all__ = [
    "User",
    "UserPreference",
    "City",
    "Attraction",
    "TransportMode",
    "TransportRoute",
    "Hotel",
    "Trip",
    "TripTransport",
    "TripHotel",
    "TripAttraction",
    "Advisory",
]
