"""
Authentication SQL Queries

Queries SQL puras para autenticación y autorización.
"""

from typing import Optional
from uuid import UUID
import asyncpg


async def authenticate_user(
    pool: asyncpg.Pool,
    email: str
) -> Optional[asyncpg.Record]:
    """
    Obtener usuario para autenticación (incluye password_hash).
    IMPORTANTE: Verificar password con bcrypt después de obtener el hash.
    """
    query = """
        SELECT
            id,
            email,
            username,
            password_hash,
            first_name,
            last_name,
            is_active,
            is_verified
        FROM users
        WHERE LOWER(email) = LOWER($1)
          AND deleted_at IS NULL
          AND is_active = TRUE
    """
    async with pool.acquire() as conn:
        return await conn.fetchrow(query, email)


async def get_user_permissions(
    pool: asyncpg.Pool,
    user_id: UUID
) -> dict:
    """
    Obtener información completa del usuario con roles para autorización.
    Retorna datos necesarios para generar JWT token.
    """
    query = """
        SELECT
            u.id,
            u.email,
            u.username,
            u.first_name,
            u.last_name,
            u.is_active,
            u.is_verified,
            COALESCE(
                json_agg(
                    r.name ORDER BY r.priority DESC
                ) FILTER (WHERE r.name IS NOT NULL),
                '[]'
            ) as roles
        FROM users u
        LEFT JOIN user_roles ur ON u.id = ur.user_id
            AND (ur.expires_at IS NULL OR ur.expires_at > NOW())
        LEFT JOIN roles r ON ur.role_id = r.id
        WHERE u.id = $1
          AND u.deleted_at IS NULL
        GROUP BY u.id
    """
    async with pool.acquire() as conn:
        return await conn.fetchrow(query, user_id)
