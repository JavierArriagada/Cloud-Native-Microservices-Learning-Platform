"""
Role Pydantic Schemas

Schemas para validación de requests/responses relacionados con roles.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field, field_validator
import re


# =============================================================================
# Base Schema
# =============================================================================

class RoleBase(BaseModel):
    """Schema base con campos comunes"""
    name: str = Field(..., min_length=2, max_length=50)
    description: Optional[str] = None
    priority: int = Field(default=0, ge=0, le=1000)

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validar que nombre de rol esté en UPPER_SNAKE_CASE"""
        if not re.match(r'^[A-Z_]+$', v):
            raise ValueError('Nombre de rol debe estar en UPPER_SNAKE_CASE (ej: ADMIN, USER, MODERATOR)')
        return v


# =============================================================================
# Create Schema (Request)
# =============================================================================

class RoleCreate(RoleBase):
    """Schema para crear rol (POST request)"""
    pass


# =============================================================================
# Update Schema (Request)
# =============================================================================

class RoleUpdate(BaseModel):
    """Schema para actualizar rol (PUT/PATCH request)"""
    name: Optional[str] = Field(None, min_length=2, max_length=50)
    description: Optional[str] = None
    priority: Optional[int] = Field(None, ge=0, le=1000)

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: Optional[str]) -> Optional[str]:
        """Validar que nombre de rol esté en UPPER_SNAKE_CASE"""
        if v is not None and not re.match(r'^[A-Z_]+$', v):
            raise ValueError('Nombre de rol debe estar en UPPER_SNAKE_CASE (ej: ADMIN, USER, MODERATOR)')
        return v


# =============================================================================
# Database Schema (Internal)
# =============================================================================

class RoleInDB(RoleBase):
    """Schema con todos los campos de la DB (uso interno)"""
    id: UUID
    is_system: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# =============================================================================
# Public Schema (Response)
# =============================================================================

class RolePublic(RoleBase):
    """Schema público (response API)"""
    id: UUID
    created_at: datetime

    model_config = {"from_attributes": True}


# =============================================================================
# Complete Schema (Response with full details)
# =============================================================================

class Role(RoleBase):
    """Schema completo con todos los campos públicos"""
    id: UUID
    is_system: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# =============================================================================
# User-Role Assignment Schemas
# =============================================================================

class UserRoleAssign(BaseModel):
    """Schema para asignar rol a usuario"""
    user_id: UUID
    role_id: UUID
    expires_at: Optional[datetime] = None


class UserRoleAssignByName(BaseModel):
    """Schema para asignar rol a usuario por nombre"""
    user_id: UUID
    role_name: str
    expires_at: Optional[datetime] = None

    @field_validator('role_name')
    @classmethod
    def validate_role_name(cls, v: str) -> str:
        """Validar formato de nombre de rol"""
        if not re.match(r'^[A-Z_]+$', v):
            raise ValueError('Nombre de rol debe estar en UPPER_SNAKE_CASE')
        return v


class UserRoleResponse(BaseModel):
    """Respuesta de asignación de rol"""
    id: UUID
    user_id: UUID
    role_id: UUID
    role_name: str
    assigned_at: datetime
    expires_at: Optional[datetime] = None
    assigned_by: Optional[UUID] = None
