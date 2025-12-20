"""
Audit Log Pydantic Schemas

Schemas para validación de requests/responses relacionados con audit logs.
NO son modelos de ORM - se usan para validar datos.
"""

from datetime import datetime
from typing import Optional, Dict, Any
from uuid import UUID
from pydantic import BaseModel, Field
from enum import Enum


class AuditActionEnum(str, Enum):
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


# Base Schema
class AuditLogBase(BaseModel):
    """Schema base con campos comunes"""
    action: AuditActionEnum
    description: str = Field(..., min_length=1, max_length=1000)
    entity_type: Optional[str] = Field(None, max_length=100)
    entity_id: Optional[UUID] = None
    extra_data: Optional[Dict[str, Any]] = None
    ip_address: Optional[str] = Field(None, max_length=45)
    user_agent: Optional[str] = None


# Create Schema (Request)
class AuditLogCreate(AuditLogBase):
    """Schema para crear audit log (POST request)"""
    user_id: Optional[UUID] = None  # Puede ser None para acciones del sistema


# Update Schema (No permitimos update de audit logs - son inmutables)
# Los audit logs NO se modifican una vez creados


# Database Schema (Internal)
class AuditLogInDB(AuditLogBase):
    """Schema con todos los campos de la DB (uso interno)"""
    id: UUID
    user_id: Optional[UUID] = None
    created_at: datetime

    model_config = {"from_attributes": True}


# Public Schema (Response)
class AuditLogPublic(AuditLogBase):
    """Schema público (response API)"""
    id: UUID
    user_id: Optional[UUID] = None
    created_at: datetime

    model_config = {"from_attributes": True}


# List Response Schema
class AuditLogListResponse(BaseModel):
    """Schema para lista paginada de audit logs"""
    logs: list[AuditLogPublic]
    total: int
    limit: int
    offset: int


# Filter Schema
class AuditLogFilter(BaseModel):
    """Schema para filtrar audit logs"""
    user_id: Optional[UUID] = None
    action: Optional[AuditActionEnum] = None
    entity_type: Optional[str] = None
    entity_id: Optional[UUID] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    limit: int = Field(default=100, le=1000)
    offset: int = Field(default=0, ge=0)
