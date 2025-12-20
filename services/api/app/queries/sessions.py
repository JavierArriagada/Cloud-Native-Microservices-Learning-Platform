"""
Session SQL Queries

Queries SQL puras para gestión de sesiones.
"""

from typing import Optional
from uuid import UUID
from datetime import datetime
import asyncpg


async def create_session(
    pool: asyncpg.Pool,
    user_id: UUID,
    session_token: str,
    refresh_token: Optional[str],
    expires_at: datetime,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None
) -> asyncpg.Record:
    """Crear nueva sesión"""
    query = """
        INSERT INTO sessions (
            user_id,
            session_token,
            refresh_token,
            expires_at,
            ip_address,
            user_agent
        )
        VALUES ($1, $2, $3, $4, $5, $6)
        RETURNING id, session_token, expires_at, created_at
    """
    async with pool.acquire() as conn:
        return await conn.fetchrow(
            query,
            user_id,
            session_token,
            refresh_token,
            expires_at,
            ip_address,
            user_agent
        )


async def get_session_by_token(
    pool: asyncpg.Pool,
    session_token: str
) -> Optional[asyncpg.Record]:
    """Obtener sesión por token y validar"""
    query = """
        SELECT
            s.id,
            s.user_id,
            s.session_token,
            s.expires_at,
            s.last_activity_at,
            u.email,
            u.username,
            u.is_active
        FROM sessions s
        JOIN users u ON s.user_id = u.id
        WHERE s.session_token = $1
          AND s.revoked_at IS NULL
          AND s.expires_at > NOW()
          AND u.is_active = TRUE
          AND u.deleted_at IS NULL
    """
    async with pool.acquire() as conn:
        return await conn.fetchrow(query, session_token)


async def update_last_activity(
    pool: asyncpg.Pool,
    session_id: UUID
) -> bool:
    """Actualizar timestamp de última actividad"""
    query = """
        UPDATE sessions
        SET last_activity_at = NOW()
        WHERE id = $1
          AND revoked_at IS NULL
        RETURNING id
    """
    async with pool.acquire() as conn:
        result = await conn.fetchrow(query, session_id)
        return result is not None


async def revoke_session(
    pool: asyncpg.Pool,
    session_token: str
) -> bool:
    """Revocar sesión (logout)"""
    query = """
        UPDATE sessions
        SET revoked_at = NOW()
        WHERE session_token = $1
          AND revoked_at IS NULL
        RETURNING id, user_id, revoked_at
    """
    async with pool.acquire() as conn:
        result = await conn.fetchrow(query, session_token)
        return result is not None


async def revoke_all_user_sessions(
    pool: asyncpg.Pool,
    user_id: UUID
) -> int:
    """Revocar todas las sesiones de un usuario"""
    query = """
        UPDATE sessions
        SET revoked_at = NOW()
        WHERE user_id = $1
          AND revoked_at IS NULL
        RETURNING id
    """
    async with pool.acquire() as conn:
        results = await conn.fetch(query, user_id)
        return len(results)


async def get_user_active_sessions(
    pool: asyncpg.Pool,
    user_id: UUID
) -> list[asyncpg.Record]:
    """Obtener sesiones activas de un usuario"""
    query = """
        SELECT
            id,
            ip_address,
            user_agent,
            created_at,
            last_activity_at,
            expires_at
        FROM sessions
        WHERE user_id = $1
          AND revoked_at IS NULL
          AND expires_at > NOW()
        ORDER BY last_activity_at DESC
    """
    async with pool.acquire() as conn:
        return await conn.fetch(query, user_id)


async def cleanup_expired_sessions(pool: asyncpg.Pool) -> int:
    """Limpiar sesiones expiradas (ejecutar periódicamente)"""
    query = """
        DELETE FROM sessions
        WHERE expires_at < NOW() - INTERVAL '7 days'
        RETURNING id
    """
    async with pool.acquire() as conn:
        results = await conn.fetch(query)
        return len(results)
