"""
Audit Log SQLAlchemy Model (SOLO PARA ALEMBIC)

Este modelo NO se usa en runtime. Solo sirve para que Alembic
pueda autogenerar migraciones.

Tabla de auditoría para registrar acciones importantes del sistema:
- Logins/logouts
- Cambios de configuración
- Operaciones CRUD en entidades importantes
- Errores y excepciones
"""

from sqlalchemy import (
    Column,
    String,
    Text,
    DateTime,
    ForeignKey,
    Index,
    Enum as SQLEnum,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
import uuid
import enum

from . import Base


class AuditAction(str, enum.Enum):
    """Tipos de acciones auditables"""
    # Autenticación
    LOGIN = "LOGIN"
    LOGOUT = "LOGOUT"
    LOGIN_FAILED = "LOGIN_FAILED"

    # CRUD Operations
    CREATE = "CREATE"
    READ = "READ"
    UPDATE = "UPDATE"
    DELETE = "DELETE"

    # Configuración
    CONFIG_CHANGE = "CONFIG_CHANGE"
    PERMISSION_CHANGE = "PERMISSION_CHANGE"

    # Sistema
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"


class AuditLog(Base):
    """Modelo SQLAlchemy de Audit Log (solo para Alembic)"""

    __tablename__ = "audit_logs"

    # Identificación
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Usuario que realizó la acción (nullable para acciones del sistema)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True
    )

    # Acción realizada
    action = Column(
        SQLEnum(AuditAction, name="audit_action_enum"),
        nullable=False,
        index=True
    )

    # Entidad afectada (nombre de la tabla)
    entity_type = Column(String(100), nullable=True, index=True)

    # ID de la entidad afectada
    entity_id = Column(UUID(as_uuid=True), nullable=True)

    # Descripción de la acción
    description = Column(Text, nullable=False)

    # Datos adicionales en formato JSON
    extra_data = Column(JSONB, nullable=True)

    # IP del cliente
    ip_address = Column(String(45), nullable=True)  # IPv6 puede ser largo

    # User Agent del cliente
    user_agent = Column(Text, nullable=True)

    # Timestamp
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        index=True
    )

    # Índices compuestos para queries comunes
    __table_args__ = (
        # Buscar por usuario y fecha
        Index("idx_audit_logs_user_created", "user_id", "created_at"),
        # Buscar por acción y fecha
        Index("idx_audit_logs_action_created", "action", "created_at"),
        # Buscar por entidad
        Index("idx_audit_logs_entity", "entity_type", "entity_id"),
        # Buscar por fecha (para limpieza de logs antiguos)
        Index("idx_audit_logs_created_at", "created_at"),
        {
            "comment": "Registro de auditoría del sistema"
        }
    )
