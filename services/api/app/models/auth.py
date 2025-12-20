"""
Authentication Pydantic Schemas

Schemas para validación de requests/responses de autenticación.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field


# =============================================================================
# Login Schemas
# =============================================================================

class LoginRequest(BaseModel):
    """Schema para request de login"""
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    """Schema para response de login"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_at: datetime
    user: "UserPublicInfo"


class UserPublicInfo(BaseModel):
    """Información pública del usuario en response de login"""
    id: UUID
    email: str
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_verified: bool
    roles: list[str] = Field(default_factory=list)


# =============================================================================
# Register Schemas
# =============================================================================

class RegisterRequest(BaseModel):
    """Schema para request de registro"""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=100)
    password: str = Field(..., min_length=8, max_length=100)
    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)


class RegisterResponse(BaseModel):
    """Schema para response de registro"""
    user: UserPublicInfo
    message: str = "Usuario creado exitosamente. Por favor verifica tu email."


# =============================================================================
# Token Schemas
# =============================================================================

class TokenData(BaseModel):
    """Datos contenidos en un JWT token"""
    user_id: UUID
    email: str
    username: str
    roles: list[str] = Field(default_factory=list)
    exp: Optional[datetime] = None  # Expiration time


class RefreshTokenRequest(BaseModel):
    """Schema para request de refresh token"""
    refresh_token: str


class RefreshTokenResponse(BaseModel):
    """Schema para response de refresh token"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_at: datetime


# =============================================================================
# Logout Schemas
# =============================================================================

class LogoutResponse(BaseModel):
    """Schema para response de logout"""
    message: str = "Sesión cerrada exitosamente"


# =============================================================================
# Email Verification Schemas
# =============================================================================

class EmailVerificationRequest(BaseModel):
    """Schema para solicitar código de verificación"""
    email: EmailStr


class EmailVerificationConfirm(BaseModel):
    """Schema para confirmar código de verificación"""
    email: EmailStr
    verification_code: str


class EmailVerificationResponse(BaseModel):
    """Schema para response de verificación de email"""
    message: str
    verified: bool


# =============================================================================
# Password Reset Schemas
# =============================================================================

class PasswordResetRequest(BaseModel):
    """Schema para solicitar reset de password"""
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    """Schema para confirmar reset de password"""
    reset_token: str
    new_password: str = Field(..., min_length=8, max_length=100)


class PasswordResetResponse(BaseModel):
    """Schema para response de reset de password"""
    message: str


# =============================================================================
# Current User Schema
# =============================================================================

class CurrentUser(BaseModel):
    """Schema del usuario actual (obtenido desde token)"""
    id: UUID
    email: str
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: bool
    is_verified: bool
    roles: list[str] = Field(default_factory=list)
