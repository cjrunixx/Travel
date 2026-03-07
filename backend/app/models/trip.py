from datetime import date, datetime

from sqlalchemy import Date, DateTime, Float, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column

from app.config.database import Base


class Trip(Base):
    __tablename__ = "trips"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    source_city_id: Mapped[int] = mapped_column(ForeignKey("cities.id"), nullable=False)
    destination_city_id: Mapped[int] = mapped_column(ForeignKey("cities.id"), nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    budget: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class TripTransport(Base):
    __tablename__ = "trip_transport"

    id: Mapped[int] = mapped_column(primary_key=True)
    trip_id: Mapped[int] = mapped_column(ForeignKey("trips.id", ondelete="CASCADE"), nullable=False)
    route_id: Mapped[int] = mapped_column(ForeignKey("transport_routes.id"), nullable=False)
    total_cost: Mapped[float] = mapped_column(Float, nullable=False)
    selected_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class TripHotel(Base):
    __tablename__ = "trip_hotels"

    id: Mapped[int] = mapped_column(primary_key=True)
    trip_id: Mapped[int] = mapped_column(ForeignKey("trips.id", ondelete="CASCADE"), nullable=False)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"), nullable=False)
    checkin_date: Mapped[date] = mapped_column(Date, nullable=False)
    checkout_date: Mapped[date] = mapped_column(Date, nullable=False)
    total_cost: Mapped[float] = mapped_column(Float, nullable=False)


class TripAttraction(Base):
    __tablename__ = "trip_attractions"
    __table_args__ = (Index("ix_trip_attractions_trip_id", "trip_id"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    trip_id: Mapped[int] = mapped_column(ForeignKey("trips.id", ondelete="CASCADE"), nullable=False)
    attraction_id: Mapped[int] = mapped_column(ForeignKey("attractions.id"), nullable=False)
    visit_date: Mapped[date | None] = mapped_column(Date, nullable=True)
