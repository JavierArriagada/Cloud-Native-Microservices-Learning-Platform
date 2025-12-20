"""
SQLAlchemy Database Models

IMPORTANTE: Estos modelos se usan EXCLUSIVAMENTE para Alembic autogenerate.
NO se deben usar como ORM en runtime.

Para queries, usar SQL puro con asyncpg (ver app/database.py).
"""

from sqlalchemy.orm import declarative_base

# Base para todos los modelos
Base = declarative_base()

# Importar todos los modelos para que Alembic los detecte
from .user import User
from .role import Role
from .user_role import UserRole
from .session import Session
from .audit_log import AuditLog, AuditAction

# Metadata para Alembic
metadata = Base.metadata

__all__ = [
    "Base",
    "metadata",
    "User",
    "Role",
    "UserRole",
    "Session",
    "AuditLog",
    "AuditAction",
]
