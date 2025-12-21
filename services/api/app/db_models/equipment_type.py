"""
Equipment Type (Tipo de Equipo) SQLAlchemy Model (SOLO PARA ALEMBIC)

Catálogo de tipos de equipos mineros e industriales.
"""
from sqlalchemy import (
    Column,
    String,
    Text,
    DateTime,
    Numeric,
    Boolean,
    Enum as SQLEnum,
    Index,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from . import Base
from .mining_enums import EquipmentCategoryEnum


class EquipmentType(Base):
    """Modelo SQLAlchemy de EquipmentType (solo para Alembic)"""

    __tablename__ = "equipment_types"

    # Identificación
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(50), nullable=False, unique=True, index=True)
    name = Column(String(255), nullable=False)

    # Categoría
    category = Column(
        SQLEnum(EquipmentCategoryEnum, name="equipment_category_enum", create_type=True),
        nullable=False
    )

    # Fabricante y Modelo
    manufacturer = Column(String(100), nullable=True)
    model = Column(String(100), nullable=True)

    # Especificaciones Técnicas
    capacity = Column(Numeric(12, 2), nullable=True)  # Capacidad nominal
    capacity_unit = Column(String(20), nullable=True)  # t, m³, kW, etc.
    power_kw = Column(Numeric(10, 2), nullable=True)  # Potencia en kW

    # Vida Útil Estimada
    expected_life_hours = Column(Numeric(10, 0), nullable=True)

    # Estado
    is_active = Column(Boolean, nullable=False, default=True, server_default="true")

    # Descripción
    description = Column(Text, nullable=True)

    # Auditoría
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        Index("idx_equipment_types_code", "code"),
        Index("idx_equipment_types_category", "category"),
        Index("idx_equipment_types_manufacturer", "manufacturer"),
        {
            "comment": "Catálogo de tipos de equipos mineros e industriales"
        }
    )
