"""
Operator (Operador) SQLAlchemy Model (SOLO PARA ALEMBIC)

Representa un operador de equipos en la operación minera.
"""
from sqlalchemy import (
    Column,
    String,
    Text,
    DateTime,
    Boolean,
    ForeignKey,
    Enum as SQLEnum,
    Index,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from . import Base
from .mining_enums import ShiftTypeEnum


class Operator(Base):
    """Modelo SQLAlchemy de Operator (solo para Alembic)"""

    __tablename__ = "operators"

    # Identificación
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    mine_id = Column(
        UUID(as_uuid=True),
        ForeignKey("mines.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # Identificación del Operador
    employee_code = Column(String(50), nullable=False, unique=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)

    # Contacto
    email = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)

    # Rol y Especialización
    job_title = Column(String(100), nullable=False)  # Operador Pala, Operador Camión, etc.
    department = Column(String(100), nullable=True)  # Mina, Planta, Mantenimiento

    # Turno Asignado
    default_shift = Column(
        SQLEnum(ShiftTypeEnum, name="shift_type_enum", create_type=True),
        nullable=True
    )

    # Certificaciones
    certifications = Column(Text, nullable=True)  # Lista de certificaciones
    license_number = Column(String(100), nullable=True)
    license_expiry_date = Column(DateTime(timezone=True), nullable=True)

    # Fechas
    hire_date = Column(DateTime(timezone=True), nullable=True)
    termination_date = Column(DateTime(timezone=True), nullable=True)

    # Estado
    is_active = Column(Boolean, nullable=False, default=True, server_default="true")

    # Descripción
    notes = Column(Text, nullable=True)

    # Auditoría
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        Index("idx_operators_mine_id", "mine_id"),
        Index("idx_operators_employee_code", "employee_code", postgresql_where=Column("deleted_at").is_(None)),
        Index("idx_operators_name", "last_name", "first_name"),
        Index("idx_operators_job_title", "job_title"),
        Index("idx_operators_is_active", "is_active", postgresql_where=Column("deleted_at").is_(None)),
        {
            "comment": "Operadores de equipos en la operación minera"
        }
    )
