"""
Block (Bloque de Minado) SQLAlchemy Model (SOLO PARA ALEMBIC)

Representa un bloque del modelo de bloques para planificación minera.
"""
from sqlalchemy import (
    Column,
    String,
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
from .mining_enums import MineralTypeEnum


class Block(Base):
    """Modelo SQLAlchemy de Block (solo para Alembic)"""

    __tablename__ = "blocks"

    # Identificación
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    mine_phase_id = Column(
        UUID(as_uuid=True),
        ForeignKey("mine_phases.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    code = Column(String(50), nullable=False, index=True)

    # Posición en el Modelo de Bloques (índices i, j, k)
    block_i = Column(Integer, nullable=False)  # Columna (Este-Oeste)
    block_j = Column(Integer, nullable=False)  # Fila (Norte-Sur)
    block_k = Column(Integer, nullable=False)  # Nivel (Elevación)

    # Coordenadas del Centroide (metros)
    centroid_x = Column(Numeric(12, 3), nullable=True)
    centroid_y = Column(Numeric(12, 3), nullable=True)
    centroid_z = Column(Numeric(10, 3), nullable=True)

    # Dimensiones del Bloque (metros)
    size_x = Column(Numeric(8, 2), nullable=False, default=10.0)
    size_y = Column(Numeric(8, 2), nullable=False, default=10.0)
    size_z = Column(Numeric(8, 2), nullable=False, default=15.0)

    # Tonelaje y Densidad
    tonnage = Column(Numeric(12, 2), nullable=True)  # Toneladas
    density = Column(Numeric(5, 3), nullable=True)   # t/m³

    # Leyes (%)
    cu_grade_pct = Column(Numeric(5, 3), nullable=True)  # Ley de cobre
    mo_grade_pct = Column(Numeric(5, 4), nullable=True)  # Ley de molibdeno
    au_grade_gpt = Column(Numeric(6, 3), nullable=True)  # Oro (gramos/tonelada)
    ag_grade_gpt = Column(Numeric(6, 2), nullable=True)  # Plata (gramos/tonelada)

    # Clasificación de Mineral
    mineral_type = Column(
        SQLEnum(MineralTypeEnum, name="mineral_type_enum", create_type=True),
        nullable=True
    )

    # Estado de Minado
    is_mined = Column(Boolean, nullable=False, default=False, server_default="false")
    mined_at = Column(DateTime(timezone=True), nullable=True)

    # Auditoría
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        CheckConstraint(
            "cu_grade_pct >= 0 AND cu_grade_pct <= 100",
            name="blocks_cu_grade_range"
        ),
        CheckConstraint(
            "mo_grade_pct >= 0 AND mo_grade_pct <= 100",
            name="blocks_mo_grade_range"
        ),
        CheckConstraint(
            "tonnage >= 0",
            name="blocks_tonnage_non_negative"
        ),
        CheckConstraint(
            "density > 0",
            name="blocks_density_positive"
        ),
        Index("idx_blocks_mine_phase_id", "mine_phase_id"),
        Index("idx_blocks_code", "code"),
        Index("idx_blocks_position", "mine_phase_id", "block_i", "block_j", "block_k"),
        Index("idx_blocks_mineral_type", "mineral_type"),
        Index("idx_blocks_is_mined", "is_mined"),
        {
            "comment": "Bloques del modelo de bloques para planificación minera"
        }
    )
