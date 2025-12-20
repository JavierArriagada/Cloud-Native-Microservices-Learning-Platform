"""
Role SQLAlchemy Model (SOLO PARA ALEMBIC)

Este modelo NO se usa en runtime. Solo sirve para que Alembic
pueda autogenerar migraciones.
"""

from sqlalchemy import (
    Column,
    String,
    Boolean,
    Integer,
    DateTime,
    Text,
    CheckConstraint,
    Index,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from . import Base


class Role(Base):
    """Modelo SQLAlchemy de Role (solo para Alembic)"""

    __tablename__ = "roles"

    # Identificación
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)

    # Configuración
    priority = Column(Integer, nullable=False, default=0, server_default="0")
    is_system = Column(Boolean, nullable=False, default=False, server_default="false")

    # Auditoría
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    # Constraints
    __table_args__ = (
        CheckConstraint(
            "name ~ '^[A-Z_]+$'",
            name="roles_name_check"
        ),
        CheckConstraint(
            "priority >= 0 AND priority <= 1000",
            name="roles_priority_check"
        ),
        Index("idx_roles_name", "name"),
        Index("idx_roles_priority", "priority"),
        {
            "comment": "Roles del sistema para RBAC"
        }
    )
