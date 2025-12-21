"""
Mineralogy (Mineralogía) SQLAlchemy Model (SOLO PARA ALEMBIC)

Representa la composición mineralógica de un yacimiento.
"""
from sqlalchemy import (
    Column,
    String,
    Text,
    DateTime,
    Numeric,
    Boolean,
    ForeignKey,
    Index,
    CheckConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from . import Base


class Mineralogy(Base):
    """Modelo SQLAlchemy de Mineralogy (solo para Alembic)"""

    __tablename__ = "mineralogy"

    # Identificación
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    deposit_id = Column(
        UUID(as_uuid=True),
        ForeignKey("deposits.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # Clasificación del Mineral
    mineral_name = Column(String(100), nullable=False)  # Ej: Calcopirita, Molibdenita
    mineral_formula = Column(String(50), nullable=True)  # Ej: CuFeS2, MoS2
    mineral_class = Column(String(50), nullable=False)  # MENA, GANGA, ALTERACION

    # Abundancia (%)
    abundance_pct = Column(Numeric(5, 2), nullable=True)  # % en volumen o peso
    is_primary_ore = Column(Boolean, nullable=False, default=False, server_default="false")

    # Propiedades de Flotación
    floatability = Column(String(20), nullable=True)  # HIGH, MEDIUM, LOW
    natural_hydrophobicity = Column(Boolean, nullable=True)

    # Asociaciones Mineralógicas
    associated_minerals = Column(Text, nullable=True)  # Lista separada por comas
    gangue_association = Column(Text, nullable=True)

    # Impurezas Críticas
    arsenic_content_ppm = Column(Numeric(8, 2), nullable=True)
    antimony_content_ppm = Column(Numeric(8, 2), nullable=True)
    bismuth_content_ppm = Column(Numeric(8, 2), nullable=True)

    # Descripción
    description = Column(Text, nullable=True)

    # Auditoría
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        CheckConstraint(
            "abundance_pct >= 0 AND abundance_pct <= 100",
            name="mineralogy_abundance_range"
        ),
        Index("idx_mineralogy_deposit_id", "deposit_id"),
        Index("idx_mineralogy_mineral_name", "mineral_name"),
        Index("idx_mineralogy_mineral_class", "mineral_class"),
        Index("idx_mineralogy_is_primary_ore", "is_primary_ore"),
        {
            "comment": "Composición mineralógica de yacimientos con propiedades de flotación"
        }
    )
