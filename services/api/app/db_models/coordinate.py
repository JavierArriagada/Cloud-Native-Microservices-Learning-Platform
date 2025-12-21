"""
Coordinate (Coordenadas Geoespaciales) SQLAlchemy Model (SOLO PARA ALEMBIC)

Representa las coordenadas geográficas de un yacimiento o punto de interés.
"""
from sqlalchemy import (
    Column,
    String,
    Text,
    DateTime,
    Numeric,
    ForeignKey,
    Index,
    CheckConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from . import Base


class Coordinate(Base):
    """Modelo SQLAlchemy de Coordinate (solo para Alembic)"""

    __tablename__ = "coordinates"

    # Identificación
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    deposit_id = Column(
        UUID(as_uuid=True),
        ForeignKey("deposits.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # Tipo de Punto
    point_type = Column(String(50), nullable=False, default="CENTROID")  # CENTROID, VERTEX, ACCESS, etc.

    # Coordenadas Geográficas (WGS84)
    latitude = Column(Numeric(10, 7), nullable=False)   # -90 a +90
    longitude = Column(Numeric(11, 7), nullable=False)  # -180 a +180
    elevation_masl = Column(Numeric(8, 2), nullable=True)  # metros sobre nivel del mar

    # Coordenadas UTM (opcional)
    utm_zone = Column(String(10), nullable=True)  # Ej: "19S"
    utm_easting = Column(Numeric(12, 3), nullable=True)
    utm_northing = Column(Numeric(13, 3), nullable=True)

    # Sistema de Referencia
    coordinate_system = Column(String(50), nullable=False, default="WGS84")
    datum = Column(String(50), nullable=True, default="WGS84")

    # Descripción
    description = Column(Text, nullable=True)

    # Auditoría
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        CheckConstraint(
            "latitude >= -90 AND latitude <= 90",
            name="coordinates_latitude_range"
        ),
        CheckConstraint(
            "longitude >= -180 AND longitude <= 180",
            name="coordinates_longitude_range"
        ),
        Index("idx_coordinates_deposit_id", "deposit_id"),
        Index("idx_coordinates_point_type", "point_type"),
        Index("idx_coordinates_lat_lon", "latitude", "longitude"),
        {
            "comment": "Coordenadas geoespaciales de yacimientos y puntos de interés"
        }
    )
