"""
Deposit (Yacimiento) SQLAlchemy Model (SOLO PARA ALEMBIC)

Representa un yacimiento minero con su clasificación geológica.
"""
from sqlalchemy import (
    Column,
    String,
    Text,
    DateTime,
    Numeric,
    Index,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from . import Base


class Deposit(Base):
    """Modelo SQLAlchemy de Deposit (solo para Alembic)"""

    __tablename__ = "deposits"

    # Identificación
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(50), nullable=False, unique=True, index=True)
    name = Column(String(255), nullable=False, index=True)

    # Clasificación Geológica
    genetic_model = Column(String(100), nullable=True)  # Pórfido cuprífero, IOCG, etc.
    primary_commodity = Column(String(50), nullable=False, default="COPPER")
    secondary_commodity = Column(String(50), nullable=True)  # Molibdeno, oro, etc.

    # Recursos y Reservas (Mt = Millones de toneladas)
    measured_resources_mt = Column(Numeric(15, 3), nullable=True)
    indicated_resources_mt = Column(Numeric(15, 3), nullable=True)
    inferred_resources_mt = Column(Numeric(15, 3), nullable=True)
    proven_reserves_mt = Column(Numeric(15, 3), nullable=True)
    probable_reserves_mt = Column(Numeric(15, 3), nullable=True)

    # Leyes Promedio (%)
    avg_cu_grade_pct = Column(Numeric(5, 3), nullable=True)  # Ej: 0.520 = 0.52%
    avg_mo_grade_pct = Column(Numeric(5, 4), nullable=True)  # Ej: 0.0150 = 150 ppm

    # Ubicación Administrativa
    country = Column(String(100), nullable=False, default="Chile")
    region = Column(String(100), nullable=True)
    province = Column(String(100), nullable=True)
    commune = Column(String(100), nullable=True)

    # Descripción
    description = Column(Text, nullable=True)

    # Auditoría
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        Index("idx_deposits_code", "code", postgresql_where=Column("deleted_at").is_(None)),
        Index("idx_deposits_name", "name", postgresql_where=Column("deleted_at").is_(None)),
        Index("idx_deposits_country_region", "country", "region"),
        {
            "comment": "Yacimientos mineros con clasificación geológica y recursos"
        }
    )
