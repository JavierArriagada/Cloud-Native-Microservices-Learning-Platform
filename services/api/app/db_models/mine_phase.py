"""
Mine Phase (Fase de Explotación) SQLAlchemy Model (SOLO PARA ALEMBIC)

Representa una fase o etapa de explotación dentro de una mina.
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
    Index,
    CheckConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from . import Base


class MinePhase(Base):
    """Modelo SQLAlchemy de MinePhase (solo para Alembic)"""

    __tablename__ = "mine_phases"

    # Identificación
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    mine_id = Column(
        UUID(as_uuid=True),
        ForeignKey("mines.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    code = Column(String(50), nullable=False, index=True)
    name = Column(String(255), nullable=False)

    # Secuencia de Explotación
    sequence_number = Column(Integer, nullable=False, default=1)

    # Parámetros de Diseño
    design_tonnage_mt = Column(Numeric(12, 3), nullable=True)  # Millones de toneladas
    design_cu_grade_pct = Column(Numeric(5, 3), nullable=True)
    design_mo_grade_pct = Column(Numeric(5, 4), nullable=True)
    design_strip_ratio = Column(Numeric(6, 2), nullable=True)  # Razón estéril/mineral

    # Elevaciones (metros sobre nivel del mar)
    elevation_top_masl = Column(Numeric(8, 2), nullable=True)
    elevation_bottom_masl = Column(Numeric(8, 2), nullable=True)

    # Fechas
    planned_start_date = Column(DateTime(timezone=True), nullable=True)
    planned_end_date = Column(DateTime(timezone=True), nullable=True)
    actual_start_date = Column(DateTime(timezone=True), nullable=True)
    actual_end_date = Column(DateTime(timezone=True), nullable=True)

    # Estado
    is_active = Column(Boolean, nullable=False, default=True, server_default="true")
    is_completed = Column(Boolean, nullable=False, default=False, server_default="false")

    # Descripción
    description = Column(Text, nullable=True)

    # Auditoría
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        CheckConstraint(
            "sequence_number > 0",
            name="mine_phases_sequence_positive"
        ),
        CheckConstraint(
            "design_cu_grade_pct >= 0 AND design_cu_grade_pct <= 100",
            name="mine_phases_cu_grade_range"
        ),
        CheckConstraint(
            "design_mo_grade_pct >= 0 AND design_mo_grade_pct <= 100",
            name="mine_phases_mo_grade_range"
        ),
        Index("idx_mine_phases_mine_id", "mine_id"),
        Index("idx_mine_phases_code", "code"),
        Index("idx_mine_phases_sequence", "mine_id", "sequence_number"),
        {
            "comment": "Fases de explotación minera con parámetros de diseño"
        }
    )
