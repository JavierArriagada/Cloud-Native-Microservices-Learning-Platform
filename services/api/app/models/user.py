"""
User Pydantic Schemas

Schemas para validación de requests/responses relacionados con usuarios.
NO son modelos de ORM - se usan para validar datos.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, field_validator
import re


# =============================================================================
# Base Schema
# =============================================================================

class UserBase(BaseModel):
    """Schema base con campos comunes"""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=100)
    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)

    @field_validator('username')
    @classmethod
    def validate_username(cls, v: str) -> str:
        """Validar que username sea alfanumérico con - y _"""
        if not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError('Username debe ser alfanumérico (puede incluir - y _)')
        return v


# =============================================================================
# Create Schema (Request)
# =============================================================================

class UserCreate(UserBase):
    """Schema para crear usuario (POST request)"""
    password: str = Field(..., min_length=8, max_length=100)

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Validar fortaleza del password"""
        if len(v) < 8:
            raise ValueError('Password debe tener al menos 8 caracteres')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password debe tener al menos una mayúscula')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password debe tener al menos una minúscula')
        if not re.search(r'[0-9]', v):
            raise ValueError('Password debe tener al menos un número')
        return v


# =============================================================================
# Update Schema (Request)
# =============================================================================

class UserUpdate(BaseModel):
    """Schema para actualizar usuario (PUT/PATCH request)"""
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=100)
    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    is_active: Optional[bool] = None

    @field_validator('username')
    @classmethod
    def validate_username(cls, v: Optional[str]) -> Optional[str]:
        """Validar que username sea alfanumérico con - y _"""
        if v is not None and not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError('Username debe ser alfanumérico (puede incluir - y _)')
        return v


# =============================================================================
# Database Schema (Internal)
# =============================================================================

class UserInDB(UserBase):
    """Schema con todos los campos de la DB (uso interno)"""
    id: UUID
    password_hash: str
    is_active: bool
    is_verified: bool
    email_verified_at: Optional[datetime] = None
    last_login_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


# =============================================================================
# Public Schema (Response)
# =============================================================================

class UserPublic(UserBase):
    """Schema público (response API, sin password)"""
    id: UUID
    is_active: bool
    is_verified: bool
    created_at: datetime

    model_config = {"from_attributes": True}


# =============================================================================
# Complete Schema (Response with full details)
# =============================================================================

class User(UserBase):
    """Schema completo con todos los campos públicos"""
    id: UUID
    is_active: bool
    is_verified: bool
    email_verified_at: Optional[datetime] = None
    last_login_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# =============================================================================
# Special Schemas
# =============================================================================

class UserWithRoles(User):
    """Usuario con sus roles asignados"""
    roles: list[str] = Field(default_factory=list)


class UserPasswordChange(BaseModel):
    """Schema para cambiar password"""
    current_password: str
    new_password: str = Field(..., min_length=8, max_length=100)

    @field_validator('new_password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Validar fortaleza del password"""
        if len(v) < 8:
            raise ValueError('Password debe tener al menos 8 caracteres')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password debe tener al menos una mayúscula')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password debe tener al menos una minúscula')
        if not re.search(r'[0-9]', v):
            raise ValueError('Password debe tener al menos un número')
        return v


class UserPasswordReset(BaseModel):
    """Schema para resetear password"""
    reset_token: str
    new_password: str = Field(..., min_length=8, max_length=100)

    @field_validator('new_password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Validar fortaleza del password"""
        if len(v) < 8:
            raise ValueError('Password debe tener al menos 8 caracteres')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password debe tener al menos una mayúscula')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password debe tener al menos una minúscula')
        if not re.search(r'[0-9]', v):
            raise ValueError('Password debe tener al menos un número')
        return v
