"""
Equipment (Equipo) SQLAlchemy Model (SOLO PARA ALEMBIC)

Representa un equipo físico en la operación minera.
"""
from sqlalchemy import (
    Column,
    String,
    Text,
    DateTime,
    Numeric,
    Boolean,
    ForeignKey,
    Enum as SQLEnum,
    Index,
    CheckConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from . import Base
from .mining_enums import EquipmentStatusEnum


class Equipment(Base):
    """Modelo SQLAlchemy de Equipment (solo para Alembic)"""

    __tablename__ = "equipment"

    # Identificación
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    equipment_type_id = Column(
        UUID(as_uuid=True),
        ForeignKey("equipment_types.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )
    mine_id = Column(
        UUID(as_uuid=True),
        ForeignKey("mines.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # Identificación del Equipo
    code = Column(String(50), nullable=False, unique=True, index=True)
    name = Column(String(255), nullable=False)
    serial_number = Column(String(100), nullable=True)
    asset_tag = Column(String(100), nullable=True)

    # Estado Operativo
    status = Column(
        SQLEnum(EquipmentStatusEnum, name="equipment_status_enum", create_type=True),
        nullable=False,
        default=EquipmentStatusEnum.OPERATIONAL
    )

    # Ubicación
    location_area = Column(String(100), nullable=True)  # Área de proceso o mina
    location_description = Column(Text, nullable=True)

    # Fechas
    installation_date = Column(DateTime(timezone=True), nullable=True)
    last_maintenance_date = Column(DateTime(timezone=True), nullable=True)
    next_maintenance_date = Column(DateTime(timezone=True), nullable=True)

    # Horas de Operación
    total_operating_hours = Column(Numeric(12, 2), nullable=False, default=0)
    hours_since_last_overhaul = Column(Numeric(12, 2), nullable=True)

    # Costo de Adquisición
    acquisition_cost = Column(Numeric(15, 2), nullable=True)
    acquisition_currency = Column(String(3), nullable=True, default="USD")

    # Estado
    is_active = Column(Boolean, nullable=False, default=True, server_default="true")

    # Descripción
    description = Column(Text, nullable=True)

    # Auditoría
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        CheckConstraint(
            "total_operating_hours >= 0",
            name="equipment_operating_hours_non_negative"
        ),
        CheckConstraint(
            "acquisition_cost >= 0",
            name="equipment_acquisition_cost_non_negative"
        ),
        Index("idx_equipment_type_id", "equipment_type_id"),
        Index("idx_equipment_mine_id", "mine_id"),
        Index("idx_equipment_code", "code", postgresql_where=Column("deleted_at").is_(None)),
        Index("idx_equipment_status", "status", postgresql_where=Column("deleted_at").is_(None)),
        Index("idx_equipment_location", "location_area"),
        {
            "comment": "Equipos físicos de la operación minera con tracking de horas y mantenimiento"
        }
    )
