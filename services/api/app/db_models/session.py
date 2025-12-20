"""
Session SQLAlchemy Model (SOLO PARA ALEMBIC)

Este modelo NO se usa en runtime. Solo sirve para que Alembic
pueda autogenerar migraciones.
"""

from sqlalchemy import (
    Column,
    String,
    DateTime,
    ForeignKey,
    CheckConstraint,
    Index,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID, INET
from sqlalchemy.sql import func
import uuid

from . import Base


class Session(Base):
    """Modelo SQLAlchemy de Session (solo para Alembic)"""

    __tablename__ = "sessions"

    # Identificación
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    # Tokens
    session_token = Column(String(500), nullable=False, unique=True)
    refresh_token = Column(String(500), nullable=True, unique=True)

    # Información de Sesión
    ip_address = Column(INET, nullable=True)
    user_agent = Column(Text, nullable=True)

    # Temporalidad
    expires_at = Column(DateTime(timezone=True), nullable=False)
    last_activity_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    revoked_at = Column(DateTime(timezone=True), nullable=True)

    # Constraints
    __table_args__ = (
        CheckConstraint(
            "expires_at > created_at",
            name="sessions_expires_check"
        ),
        Index(
            "idx_sessions_user_id",
            "user_id",
            postgresql_where=Column("revoked_at").is_(None)
        ),
        Index(
            "idx_sessions_session_token",
            "session_token",
            postgresql_where=Column("revoked_at").is_(None)
        ),
        Index(
            "idx_sessions_refresh_token",
            "refresh_token",
            postgresql_where=(Column("revoked_at").is_(None)) & (Column("refresh_token").isnot(None))
        ),
        Index(
            "idx_sessions_expires_at",
            "expires_at",
            postgresql_where=Column("revoked_at").is_(None)
        ),
        {
            "comment": "Sesiones activas de usuarios (JWT, refresh tokens)"
        }
    )
