"""
User SQLAlchemy Model (SOLO PARA ALEMBIC)

Este modelo NO se usa en runtime. Solo sirve para que Alembic
pueda autogenerar migraciones.
"""

from datetime import datetime
from sqlalchemy import (
    Column,
    String,
    Boolean,
    DateTime,
    CheckConstraint,
    Index,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from . import Base


class User(Base):
    """Modelo SQLAlchemy de User (solo para Alembic)"""

    __tablename__ = "users"

    # Identificación
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), nullable=False, unique=True, index=True)
    username = Column(String(100), nullable=False, unique=True, index=True)
    password_hash = Column(String(255), nullable=False)

    # Información Personal
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)

    # Estado del Usuario
    is_active = Column(Boolean, nullable=False, default=True, server_default="true")
    is_verified = Column(Boolean, nullable=False, default=False, server_default="false")
    email_verified_at = Column(DateTime(timezone=True), nullable=True)
    last_login_at = Column(DateTime(timezone=True), nullable=True)

    # Auditoría
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    # Constraints
    __table_args__ = (
        CheckConstraint(
            "email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$'",
            name="users_email_check"
        ),
        CheckConstraint(
            "LENGTH(username) >= 3 AND username ~ '^[a-zA-Z0-9_-]+$'",
            name="users_username_check"
        ),
        Index("idx_users_email", "email", postgresql_where=Column("deleted_at").is_(None)),
        Index("idx_users_username", "username", postgresql_where=Column("deleted_at").is_(None)),
        Index("idx_users_is_active", "is_active", postgresql_where=Column("deleted_at").is_(None)),
        Index("idx_users_created_at", "created_at"),
        {
            "comment": "Tabla principal de usuarios del sistema"
        }
    )
