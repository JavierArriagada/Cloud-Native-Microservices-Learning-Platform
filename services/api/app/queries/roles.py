"""
Role SQL Queries

Queries SQL puras para operaciones de roles.
"""

from typing import Optional
from uuid import UUID
import asyncpg


async def get_all_roles(pool: asyncpg.Pool) -> list[asyncpg.Record]:
    """Obtener todos los roles ordenados por prioridad"""
    query = """
        SELECT
            id,
            name,
            description,
            priority,
            is_system,
            created_at
        FROM roles
        ORDER BY priority DESC
    """
    async with pool.acquire() as conn:
        return await conn.fetch(query)


async def get_role_by_name(pool: asyncpg.Pool, name: str) -> Optional[asyncpg.Record]:
    """Obtener rol por nombre"""
    query = """
        SELECT
            id,
            name,
            description,
            priority,
            is_system,
            created_at
        FROM roles
        WHERE name = $1
    """
    async with pool.acquire() as conn:
        return await conn.fetchrow(query, name.upper())


async def assign_role_to_user(
    pool: asyncpg.Pool,
    user_id: UUID,
    role_id: UUID,
    assigned_by: Optional[UUID] = None
) -> asyncpg.Record:
    """Asignar rol a usuario"""
    query = """
        INSERT INTO user_roles (user_id, role_id, assigned_by)
        VALUES ($1, $2, $3)
        ON CONFLICT (user_id, role_id) DO NOTHING
        RETURNING id, assigned_at
    """
    async with pool.acquire() as conn:
        return await conn.fetchrow(query, user_id, role_id, assigned_by)


async def remove_role_from_user(
    pool: asyncpg.Pool,
    user_id: UUID,
    role_id: UUID
) -> bool:
    """Remover rol de usuario"""
    query = """
        DELETE FROM user_roles
        WHERE user_id = $1 AND role_id = $2
        RETURNING id
    """
    async with pool.acquire() as conn:
        result = await conn.fetchrow(query, user_id, role_id)
        return result is not None


async def get_user_roles(pool: asyncpg.Pool, user_id: UUID) -> list[str]:
    """Obtener nombres de roles de un usuario"""
    query = """
        SELECT r.name
        FROM user_roles ur
        JOIN roles r ON ur.role_id = r.id
        WHERE ur.user_id = $1
          AND (ur.expires_at IS NULL OR ur.expires_at > NOW())
        ORDER BY r.priority DESC
    """
    async with pool.acquire() as conn:
        rows = await conn.fetch(query, user_id)
        return [row["name"] for row in rows]


async def check_user_has_role(
    pool: asyncpg.Pool,
    user_id: UUID,
    role_name: str
) -> bool:
    """Verificar si usuario tiene un rol específico"""
    query = """
        SELECT EXISTS(
            SELECT 1
            FROM user_roles ur
            JOIN roles r ON ur.role_id = r.id
            WHERE ur.user_id = $1
              AND r.name = $2
              AND (ur.expires_at IS NULL OR ur.expires_at > NOW())
        )
    """
    async with pool.acquire() as conn:
        return await conn.fetchval(query, user_id, role_name.upper())
