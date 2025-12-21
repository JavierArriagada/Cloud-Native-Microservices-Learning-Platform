"""
Reagent (Reactivo Químico) SQLAlchemy Model (SOLO PARA ALEMBIC)

Catálogo de reactivos químicos utilizados en el proceso de flotación.
"""
from sqlalchemy import (
    Column,
    String,
    Text,
    DateTime,
    Numeric,
    Boolean,
    Index,
    CheckConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from . import Base


class Reagent(Base):
    """Modelo SQLAlchemy de Reagent (solo para Alembic)"""

    __tablename__ = "reagents"

    # Identificación
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(50), nullable=False, unique=True, index=True)
    name = Column(String(255), nullable=False)
    commercial_name = Column(String(255), nullable=True)

    # Clasificación
    reagent_type = Column(String(50), nullable=False)  # COLLECTOR, FROTHER, DEPRESSANT, ACTIVATOR, PH_MODIFIER
    chemical_family = Column(String(100), nullable=True)  # Xantatos, Ditiofosfatos, etc.

    # Propiedades Químicas
    chemical_formula = Column(String(100), nullable=True)
    molecular_weight = Column(Numeric(10, 4), nullable=True)
    density = Column(Numeric(6, 4), nullable=True)  # g/cm³
    ph = Column(Numeric(4, 2), nullable=True)

    # Dosificación Recomendada
    recommended_dosage_min = Column(Numeric(10, 4), nullable=True)  # g/t
    recommended_dosage_max = Column(Numeric(10, 4), nullable=True)
    dosage_unit = Column(String(20), nullable=True, default="g/t")

    # Costo
    unit_cost = Column(Numeric(12, 4), nullable=True)
    cost_currency = Column(String(3), nullable=True, default="USD")
    cost_unit = Column(String(20), nullable=True, default="kg")

    # Proveedor
    supplier = Column(String(255), nullable=True)
    supplier_code = Column(String(100), nullable=True)

    # Seguridad
    hazard_class = Column(String(50), nullable=True)
    storage_requirements = Column(Text, nullable=True)

    # Estado
    is_active = Column(Boolean, nullable=False, default=True, server_default="true")

    # Descripción
    description = Column(Text, nullable=True)
    application_notes = Column(Text, nullable=True)

    # Auditoría
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        CheckConstraint(
            "recommended_dosage_min >= 0",
            name="reagents_dosage_min_non_negative"
        ),
        CheckConstraint(
            "recommended_dosage_max >= recommended_dosage_min",
            name="reagents_dosage_max_gte_min"
        ),
        CheckConstraint(
            "unit_cost >= 0",
            name="reagents_unit_cost_non_negative"
        ),
        Index("idx_reagents_code", "code"),
        Index("idx_reagents_reagent_type", "reagent_type"),
        Index("idx_reagents_chemical_family", "chemical_family"),
        Index("idx_reagents_is_active", "is_active"),
        {
            "comment": "Catálogo de reactivos químicos para proceso de flotación"
        }
    )
