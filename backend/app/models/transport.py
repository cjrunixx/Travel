from sqlalchemy import Float, ForeignKey, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.config.database import Base


class TransportMode(Base):
    __tablename__ = "transport_modes"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)


class TransportRoute(Base):
    __tablename__ = "transport_routes"
    __table_args__ = (Index("ix_routes_source_destination", "source_city_id", "destination_city_id"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    source_city_id: Mapped[int] = mapped_column(ForeignKey("cities.id"), nullable=False)
    destination_city_id: Mapped[int] = mapped_column(ForeignKey("cities.id"), nullable=False)
    transport_mode_id: Mapped[int] = mapped_column(ForeignKey("transport_modes.id"), nullable=False)
    duration_minutes: Mapped[int] = mapped_column(Integer, nullable=False)
    distance_km: Mapped[float] = mapped_column(Float, nullable=False)
    base_cost: Mapped[float] = mapped_column(Float, nullable=False)
    stops: Mapped[int] = mapped_column(Integer, default=0)
