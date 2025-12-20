"""
Pydantic Models/Schemas

IMPORTANTE: Estos NO son modelos de ORM.
Son schemas de Pydantic para validación de requests/responses.

Las queries a la base de datos se hacen con SQL puro usando asyncpg.
"""

from .user import (
    User,
    UserCreate,
    UserUpdate,
    UserInDB,
    UserPublic,
)
from .role import (
    Role,
    RoleCreate,
    RoleUpdate,
    RoleInDB,
    RolePublic,
)
from .session import (
    Session,
    SessionCreate,
    SessionInDB,
    SessionPublic,
)
from .auth import (
    LoginRequest,
    LoginResponse,
    RegisterRequest,
    RegisterResponse,
    TokenData,
    RefreshTokenRequest,
)

__all__ = [
    # User
    "User",
    "UserCreate",
    "UserUpdate",
    "UserInDB",
    "UserPublic",
    # Role
    "Role",
    "RoleCreate",
    "RoleUpdate",
    "RoleInDB",
    "RolePublic",
    # Session
    "Session",
    "SessionCreate",
    "SessionInDB",
    "SessionPublic",
    # Auth
    "LoginRequest",
    "LoginResponse",
    "RegisterRequest",
    "RegisterResponse",
    "TokenData",
    "RefreshTokenRequest",
]
