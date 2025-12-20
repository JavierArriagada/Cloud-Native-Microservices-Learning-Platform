"""
User SQL Queries

Queries SQL puras para operaciones CRUD de usuarios.
Ejecutar con asyncpg usando los helpers en app/database.py
"""

from typing import Optional
from uuid import UUID
from datetime import datetime
import asyncpg


# =============================================================================
# READ QUERIES
# =============================================================================

async def get_user_by_id(pool: asyncpg.Pool, user_id: UUID) -> Optional[asyncpg.Record]:
    """Obtener usuario por ID"""
    query = """
        SELECT
            id,
            email,
            username,
            password_hash,
            first_name,
            last_name,
            is_active,
            is_verified,
            email_verified_at,
            last_login_at,
            created_at,
            updated_at
        FROM users
        WHERE id = $1
          AND deleted_at IS NULL
    """
    async with pool.acquire() as conn:
        return await conn.fetchrow(query, user_id)


async def get_user_by_email(pool: asyncpg.Pool, email: str) -> Optional[asyncpg.Record]:
    """Obtener usuario por email (para login)"""
    query = """
        SELECT
            id,
            email,
            username,
            password_hash,
            first_name,
            last_name,
            is_active,
            is_verified,
            email_verified_at,
            last_login_at,
            created_at,
            updated_at
        FROM users
        WHERE LOWER(email) = LOWER($1)
          AND deleted_at IS NULL
    """
    async with pool.acquire() as conn:
        return await conn.fetchrow(query, email)


async def get_user_by_username(pool: asyncpg.Pool, username: str) -> Optional[asyncpg.Record]:
    """Obtener usuario por username"""
    query = """
        SELECT
            id,
            email,
            username,
            password_hash,
            first_name,
            last_name,
            is_active,
            is_verified,
            email_verified_at,
            last_login_at,
            created_at,
            updated_at
        FROM users
        WHERE LOWER(username) = LOWER($1)
          AND deleted_at IS NULL
    """
    async with pool.acquire() as conn:
        return await conn.fetchrow(query, username)


async def get_all_users(
    pool: asyncpg.Pool,
    limit: int = 100,
    offset: int = 0,
    is_active: Optional[bool] = None
) -> list[asyncpg.Record]:
    """Obtener lista de usuarios con paginación"""
    query = """
        SELECT
            id,
            email,
            username,
            first_name,
            last_name,
            is_active,
            is_verified,
            created_at,
            last_login_at
        FROM users
        WHERE deleted_at IS NULL
          AND ($3::boolean IS NULL OR is_active = $3)
        ORDER BY created_at DESC
        LIMIT $1 OFFSET $2
    """
    async with pool.acquire() as conn:
        return await conn.fetch(query, limit, offset, is_active)


async def count_users(pool: asyncpg.Pool, is_active: Optional[bool] = None) -> int:
    """Contar usuarios"""
    query = """
        SELECT COUNT(*)
        FROM users
        WHERE deleted_at IS NULL
          AND ($1::boolean IS NULL OR is_active = $1)
    """
    async with pool.acquire() as conn:
        return await conn.fetchval(query, is_active)


async def get_user_with_roles(pool: asyncpg.Pool, user_id: UUID) -> Optional[dict]:
    """Obtener usuario con sus roles"""
    user_query = """
        SELECT
            id,
            email,
            username,
            first_name,
            last_name,
            is_active,
            is_verified,
            created_at,
            updated_at
        FROM users
        WHERE id = $1
          AND deleted_at IS NULL
    """

    roles_query = """
        SELECT r.name, r.priority, ur.expires_at
        FROM user_roles ur
        JOIN roles r ON ur.role_id = r.id
        WHERE ur.user_id = $1
          AND (ur.expires_at IS NULL OR ur.expires_at > NOW())
        ORDER BY r.priority DESC
    """

    async with pool.acquire() as conn:
        user = await conn.fetchrow(user_query, user_id)
        if not user:
            return None

        roles = await conn.fetch(roles_query, user_id)

        return {
            **dict(user),
            "roles": [dict(role) for role in roles]
        }


# =============================================================================
# CREATE QUERIES
# =============================================================================

async def create_user(
    pool: asyncpg.Pool,
    email: str,
    username: str,
    password_hash: str,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None
) -> asyncpg.Record:
    """Crear nuevo usuario"""
    query = """
        INSERT INTO users (
            email,
            username,
            password_hash,
            first_name,
            last_name
        )
        VALUES ($1, $2, $3, $4, $5)
        RETURNING
            id,
            email,
            username,
            first_name,
            last_name,
            is_active,
            is_verified,
            created_at
    """
    async with pool.acquire() as conn:
        return await conn.fetchrow(
            query,
            email.lower(),
            username,
            password_hash,
            first_name,
            last_name
        )


# =============================================================================
# UPDATE QUERIES
# =============================================================================

async def update_user(
    pool: asyncpg.Pool,
    user_id: UUID,
    email: Optional[str] = None,
    username: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    is_active: Optional[bool] = None
) -> Optional[asyncpg.Record]:
    """Actualizar información del usuario"""
    query = """
        UPDATE users
        SET
            email = COALESCE($2, email),
            username = COALESCE($3, username),
            first_name = COALESCE($4, first_name),
            last_name = COALESCE($5, last_name),
            is_active = COALESCE($6, is_active),
            updated_at = NOW()
        WHERE id = $1
          AND deleted_at IS NULL
        RETURNING
            id,
            email,
            username,
            first_name,
            last_name,
            is_active,
            is_verified,
            updated_at
    """
    async with pool.acquire() as conn:
        return await conn.fetchrow(
            query,
            user_id,
            email.lower() if email else None,
            username,
            first_name,
            last_name,
            is_active
        )


async def update_user_password(
    pool: asyncpg.Pool,
    user_id: UUID,
    new_password_hash: str
) -> bool:
    """Actualizar password del usuario"""
    query = """
        UPDATE users
        SET
            password_hash = $2,
            updated_at = NOW()
        WHERE id = $1
          AND deleted_at IS NULL
        RETURNING id
    """
    async with pool.acquire() as conn:
        result = await conn.fetchrow(query, user_id, new_password_hash)
        return result is not None


async def mark_email_verified(
    pool: asyncpg.Pool,
    user_id: UUID
) -> bool:
    """Marcar email como verificado"""
    query = """
        UPDATE users
        SET
            is_verified = TRUE,
            email_verified_at = NOW(),
            updated_at = NOW()
        WHERE id = $1
          AND deleted_at IS NULL
        RETURNING id
    """
    async with pool.acquire() as conn:
        result = await conn.fetchrow(query, user_id)
        return result is not None


async def update_last_login(
    pool: asyncpg.Pool,
    user_id: UUID
) -> bool:
    """Actualizar timestamp de último login"""
    query = """
        UPDATE users
        SET
            last_login_at = NOW(),
            updated_at = NOW()
        WHERE id = $1
          AND deleted_at IS NULL
        RETURNING id
    """
    async with pool.acquire() as conn:
        result = await conn.fetchrow(query, user_id)
        return result is not None


# =============================================================================
# DELETE QUERIES
# =============================================================================

async def soft_delete_user(
    pool: asyncpg.Pool,
    user_id: UUID
) -> bool:
    """Soft delete de usuario (no elimina físicamente)"""
    query = """
        UPDATE users
        SET
            deleted_at = NOW(),
            updated_at = NOW()
        WHERE id = $1
          AND deleted_at IS NULL
        RETURNING id, email, deleted_at
    """
    async with pool.acquire() as conn:
        result = await conn.fetchrow(query, user_id)
        return result is not None


async def hard_delete_user(
    pool: asyncpg.Pool,
    user_id: UUID
) -> bool:
    """Hard delete de usuario (PELIGRO: elimina permanentemente)"""
    query = """
        DELETE FROM users
        WHERE id = $1
        RETURNING id
    """
    async with pool.acquire() as conn:
        result = await conn.fetchrow(query, user_id)
        return result is not None


# =============================================================================
# VALIDATION QUERIES
# =============================================================================

async def check_email_exists(pool: asyncpg.Pool, email: str) -> bool:
    """Verificar si email ya existe"""
    query = """
        SELECT EXISTS(
            SELECT 1
            FROM users
            WHERE LOWER(email) = LOWER($1)
              AND deleted_at IS NULL
        )
    """
    async with pool.acquire() as conn:
        return await conn.fetchval(query, email)


async def check_username_exists(pool: asyncpg.Pool, username: str) -> bool:
    """Verificar si username ya existe"""
    query = """
        SELECT EXISTS(
            SELECT 1
            FROM users
            WHERE LOWER(username) = LOWER($1)
              AND deleted_at IS NULL
        )
    """
    async with pool.acquire() as conn:
        return await conn.fetchval(query, username)


# =============================================================================
# SEARCH QUERIES
# =============================================================================

async def search_users(
    pool: asyncpg.Pool,
    search_term: str,
    limit: int = 20
) -> list[asyncpg.Record]:
    """Buscar usuarios por email, username o nombre"""
    query = """
        SELECT
            id,
            email,
            username,
            first_name,
            last_name,
            is_active,
            created_at
        FROM users
        WHERE deleted_at IS NULL
          AND (
              LOWER(email) LIKE LOWER($1) OR
              LOWER(username) LIKE LOWER($1) OR
              LOWER(first_name) LIKE LOWER($1) OR
              LOWER(last_name) LIKE LOWER($1)
          )
        ORDER BY created_at DESC
        LIMIT $2
    """
    search_pattern = f"%{search_term}%"
    async with pool.acquire() as conn:
        return await conn.fetch(query, search_pattern, limit)
