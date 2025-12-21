"""
Mine (Mina) SQLAlchemy Model (SOLO PARA ALEMBIC)

Representa una operación minera asociada a un yacimiento.
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
from .mining_enums import MineTypeEnum


class Mine(Base):
    """Modelo SQLAlchemy de Mine (solo para Alembic)"""

    __tablename__ = "mines"

    # Identificación
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    deposit_id = Column(
        UUID(as_uuid=True),
        ForeignKey("deposits.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )
    code = Column(String(50), nullable=False, unique=True, index=True)
    name = Column(String(255), nullable=False, index=True)

    # Tipo de Explotación
    mine_type = Column(
        SQLEnum(MineTypeEnum, name="mine_type_enum", create_type=True),
        nullable=False,
        default=MineTypeEnum.OPEN_PIT
    )

    # Capacidad de Producción
    design_capacity_tpd = Column(Numeric(12, 2), nullable=True)  # Toneladas por día
    current_capacity_tpd = Column(Numeric(12, 2), nullable=True)

    # Fechas Operativas
    start_date = Column(DateTime(timezone=True), nullable=True)
    expected_end_date = Column(DateTime(timezone=True), nullable=True)

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
            "design_capacity_tpd > 0",
            name="mines_design_capacity_positive"
        ),
        CheckConstraint(
            "current_capacity_tpd >= 0",
            name="mines_current_capacity_non_negative"
        ),
        Index("idx_mines_deposit_id", "deposit_id"),
        Index("idx_mines_code", "code", postgresql_where=Column("deleted_at").is_(None)),
        Index("idx_mines_is_active", "is_active", postgresql_where=Column("deleted_at").is_(None)),
        {
            "comment": "Operaciones mineras asociadas a yacimientos"
        }
    )
