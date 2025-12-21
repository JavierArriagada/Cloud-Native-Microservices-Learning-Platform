"""
Process Area (Área de Proceso) SQLAlchemy Model (SOLO PARA ALEMBIC)

Representa un área o etapa del proceso de concentración.
"""
from sqlalchemy import (
    Column,
    String,
    Text,
    DateTime,
    Numeric,
    Integer,
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
from .mining_enums import ProcessAreaTypeEnum


class ProcessArea(Base):
    """Modelo SQLAlchemy de ProcessArea (solo para Alembic)"""

    __tablename__ = "process_areas"

    # Identificación
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    mine_id = Column(
        UUID(as_uuid=True),
        ForeignKey("mines.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    parent_area_id = Column(
        UUID(as_uuid=True),
        ForeignKey("process_areas.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )

    # Identificación del Área
    code = Column(String(50), nullable=False, index=True)
    name = Column(String(255), nullable=False)

    # Tipo de Proceso
    area_type = Column(
        SQLEnum(ProcessAreaTypeEnum, name="process_area_type_enum", create_type=True),
        nullable=False
    )

    # Secuencia en el Flujo de Proceso
    sequence_order = Column(Integer, nullable=False, default=1)

    # Capacidad de Diseño
    design_capacity = Column(Numeric(12, 2), nullable=True)
    capacity_unit = Column(String(20), nullable=True, default="tph")  # toneladas por hora

    # Parámetros de Operación Objetivo
    target_recovery_pct = Column(Numeric(5, 2), nullable=True)  # Recuperación objetivo
    target_grade_pct = Column(Numeric(5, 3), nullable=True)     # Ley objetivo

    # Circuito (para flotación)
    circuit_type = Column(String(50), nullable=True)  # COLLECTIVE, SELECTIVE_CU, SELECTIVE_MO

    # Estado
    is_active = Column(Boolean, nullable=False, default=True, server_default="true")

    # Descripción
    description = Column(Text, nullable=True)

    # Auditoría
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        CheckConstraint(
            "target_recovery_pct >= 0 AND target_recovery_pct <= 100",
            name="process_areas_recovery_range"
        ),
        CheckConstraint(
            "target_grade_pct >= 0 AND target_grade_pct <= 100",
            name="process_areas_grade_range"
        ),
        CheckConstraint(
            "sequence_order > 0",
            name="process_areas_sequence_positive"
        ),
        Index("idx_process_areas_mine_id", "mine_id"),
        Index("idx_process_areas_code", "code"),
        Index("idx_process_areas_area_type", "area_type"),
        Index("idx_process_areas_sequence", "mine_id", "sequence_order"),
        Index("idx_process_areas_parent", "parent_area_id"),
        {
            "comment": "Áreas de proceso de la planta concentradora"
        }
    )
