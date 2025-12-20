"""
Session Pydantic Schemas

Schemas para validación de requests/responses relacionados con sesiones.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field


# =============================================================================
# Base Schema
# =============================================================================

class SessionBase(BaseModel):
    """Schema base con campos comunes"""
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None


# =============================================================================
# Create Schema (Internal)
# =============================================================================

class SessionCreate(SessionBase):
    """Schema para crear sesión (uso interno)"""
    user_id: UUID
    session_token: str
    refresh_token: Optional[str] = None
    expires_at: datetime


# =============================================================================
# Database Schema (Internal)
# =============================================================================

class SessionInDB(SessionBase):
    """Schema con todos los campos de la DB (uso interno)"""
    id: UUID
    user_id: UUID
    session_token: str
    refresh_token: Optional[str] = None
    expires_at: datetime
    last_activity_at: datetime
    created_at: datetime
    revoked_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


# =============================================================================
# Public Schema (Response)
# =============================================================================

class SessionPublic(SessionBase):
    """Schema público (response API)"""
    id: UUID
    expires_at: datetime
    last_activity_at: datetime
    created_at: datetime

    model_config = {"from_attributes": True}


# =============================================================================
# Complete Schema (Response)
# =============================================================================

class Session(SessionBase):
    """Schema completo con todos los campos públicos"""
    id: UUID
    user_id: UUID
    expires_at: datetime
    last_activity_at: datetime
    created_at: datetime
    revoked_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


# =============================================================================
# Token Validation Response
# =============================================================================

class TokenValidationResponse(BaseModel):
    """Respuesta de validación de token"""
    valid: bool
    user_id: Optional[UUID] = None
    email: Optional[str] = None
    username: Optional[str] = None
    expires_at: Optional[datetime] = None
    error: Optional[str] = None


# =============================================================================
# Session List Item
# =============================================================================

class SessionListItem(SessionBase):
    """Item de lista de sesiones (para mostrar sesiones activas del usuario)"""
    id: UUID
    created_at: datetime
    last_activity_at: datetime
    expires_at: datetime
    is_current: bool = Field(default=False, description="Si es la sesión actual")

    model_config = {"from_attributes": True}
