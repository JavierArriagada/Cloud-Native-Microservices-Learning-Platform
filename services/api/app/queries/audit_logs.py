"""
Audit Log SQL Queries

Queries SQL puras para operaciones CRUD de audit logs.
Ejecutar con asyncpg usando los helpers en app/database.py
"""

from typing import Optional
from uuid import UUID
from datetime import datetime
import asyncpg


# ============================================================================
# READ QUERIES
# ============================================================================

async def get_audit_log_by_id(pool: asyncpg.Pool, log_id: UUID) -> Optional[asyncpg.Record]:
    """Obtener audit log por ID"""
    query = """
        SELECT
            id,
            user_id,
            action,
            entity_type,
            entity_id,
            description,
            extra_data,
            ip_address,
            user_agent,
            created_at
        FROM audit_logs
        WHERE id = $1
    """
    async with pool.acquire() as conn:
        return await conn.fetchrow(query, log_id)


async def get_audit_logs(
    pool: asyncpg.Pool,
    user_id: Optional[UUID] = None,
    action: Optional[str] = None,
    entity_type: Optional[str] = None,
    entity_id: Optional[UUID] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    limit: int = 100,
    offset: int = 0
) -> list[asyncpg.Record]:
    """
    Obtener audit logs con filtros opcionales

    Args:
        pool: Connection pool
        user_id: Filtrar por usuario
        action: Filtrar por tipo de acción
        entity_type: Filtrar por tipo de entidad
        entity_id: Filtrar por ID de entidad
        start_date: Fecha de inicio
        end_date: Fecha de fin
        limit: Límite de resultados
        offset: Offset para paginación
    """
    query = """
        SELECT
            id,
            user_id,
            action,
            entity_type,
            entity_id,
            description,
            extra_data,
            ip_address,
            user_agent,
            created_at
        FROM audit_logs
        WHERE ($1::uuid IS NULL OR user_id = $1)
          AND ($2::text IS NULL OR action = $2)
          AND ($3::text IS NULL OR entity_type = $3)
          AND ($4::uuid IS NULL OR entity_id = $4)
          AND ($5::timestamp IS NULL OR created_at >= $5)
          AND ($6::timestamp IS NULL OR created_at <= $6)
        ORDER BY created_at DESC
        LIMIT $7 OFFSET $8
    """
    async with pool.acquire() as conn:
        return await conn.fetch(
            query,
            user_id,
            action,
            entity_type,
            entity_id,
            start_date,
            end_date,
            limit,
            offset
        )


async def count_audit_logs(
    pool: asyncpg.Pool,
    user_id: Optional[UUID] = None,
    action: Optional[str] = None,
    entity_type: Optional[str] = None,
    entity_id: Optional[UUID] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> int:
    """Contar audit logs con filtros opcionales"""
    query = """
        SELECT COUNT(*)
        FROM audit_logs
        WHERE ($1::uuid IS NULL OR user_id = $1)
          AND ($2::text IS NULL OR action = $2)
          AND ($3::text IS NULL OR entity_type = $3)
          AND ($4::uuid IS NULL OR entity_id = $4)
          AND ($5::timestamp IS NULL OR created_at >= $5)
          AND ($6::timestamp IS NULL OR created_at <= $6)
    """
    async with pool.acquire() as conn:
        result = await conn.fetchval(
            query,
            user_id,
            action,
            entity_type,
            entity_id,
            start_date,
            end_date
        )
        return result or 0


async def get_recent_audit_logs_by_user(
    pool: asyncpg.Pool,
    user_id: UUID,
    limit: int = 50
) -> list[asyncpg.Record]:
    """Obtener logs recientes de un usuario específico"""
    query = """
        SELECT
            id,
            action,
            entity_type,
            entity_id,
            description,
            ip_address,
            created_at
        FROM audit_logs
        WHERE user_id = $1
        ORDER BY created_at DESC
        LIMIT $2
    """
    async with pool.acquire() as conn:
        return await conn.fetch(query, user_id, limit)


async def get_audit_logs_by_entity(
    pool: asyncpg.Pool,
    entity_type: str,
    entity_id: UUID,
    limit: int = 100
) -> list[asyncpg.Record]:
    """Obtener todos los audit logs de una entidad específica"""
    query = """
        SELECT
            id,
            user_id,
            action,
            description,
            extra_data,
            created_at
        FROM audit_logs
        WHERE entity_type = $1
          AND entity_id = $2
        ORDER BY created_at DESC
        LIMIT $3
    """
    async with pool.acquire() as conn:
        return await conn.fetch(query, entity_type, entity_id, limit)


# ============================================================================
# CREATE QUERIES
# ============================================================================

async def create_audit_log(
    pool: asyncpg.Pool,
    action: str,
    description: str,
    user_id: Optional[UUID] = None,
    entity_type: Optional[str] = None,
    entity_id: Optional[UUID] = None,
    extra_data: Optional[dict] = None,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None
) -> asyncpg.Record:
    """
    Crear nuevo audit log

    Args:
        pool: Connection pool
        action: Tipo de acción (LOGIN, CREATE, UPDATE, etc.)
        description: Descripción de la acción
        user_id: ID del usuario (None para acciones del sistema)
        entity_type: Tipo de entidad afectada
        entity_id: ID de la entidad afectada
        extra_data: Datos adicionales en JSON
        ip_address: IP del cliente
        user_agent: User agent del cliente
    """
    query = """
        INSERT INTO audit_logs (
            user_id,
            action,
            entity_type,
            entity_id,
            description,
            extra_data,
            ip_address,
            user_agent
        )
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
        RETURNING
            id,
            user_id,
            action,
            entity_type,
            entity_id,
            description,
            extra_data,
            ip_address,
            user_agent,
            created_at
    """
    async with pool.acquire() as conn:
        return await conn.fetchrow(
            query,
            user_id,
            action,
            entity_type,
            entity_id,
            description,
            extra_data,
            ip_address,
            user_agent
        )


# ============================================================================
# DELETE QUERIES (para limpieza de logs antiguos)
# ============================================================================

async def delete_old_audit_logs(
    pool: asyncpg.Pool,
    days_to_keep: int = 90
) -> int:
    """
    Eliminar audit logs antiguos

    Args:
        pool: Connection pool
        days_to_keep: Días a mantener (default: 90)

    Returns:
        Número de registros eliminados
    """
    query = """
        DELETE FROM audit_logs
        WHERE created_at < NOW() - INTERVAL '1 day' * $1
        RETURNING id
    """
    async with pool.acquire() as conn:
        result = await conn.fetch(query, days_to_keep)
        return len(result)


async def delete_audit_logs_by_entity(
    pool: asyncpg.Pool,
    entity_type: str,
    entity_id: UUID
) -> int:
    """
    Eliminar todos los audit logs de una entidad específica
    Útil cuando se elimina una entidad del sistema
    """
    query = """
        DELETE FROM audit_logs
        WHERE entity_type = $1
          AND entity_id = $2
        RETURNING id
    """
    async with pool.acquire() as conn:
        result = await conn.fetch(query, entity_type, entity_id)
        return len(result)


# ============================================================================
# UTILITY QUERIES
# ============================================================================

async def get_audit_log_statistics(
    pool: asyncpg.Pool,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> asyncpg.Record:
    """Obtener estadísticas de audit logs por tipo de acción"""
    query = """
        SELECT
            action,
            COUNT(*) as count,
            COUNT(DISTINCT user_id) as unique_users,
            MIN(created_at) as first_occurrence,
            MAX(created_at) as last_occurrence
        FROM audit_logs
        WHERE ($1::timestamp IS NULL OR created_at >= $1)
          AND ($2::timestamp IS NULL OR created_at <= $2)
        GROUP BY action
        ORDER BY count DESC
    """
    async with pool.acquire() as conn:
        return await conn.fetch(query, start_date, end_date)


async def get_most_active_users(
    pool: asyncpg.Pool,
    limit: int = 10,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> list[asyncpg.Record]:
    """Obtener usuarios más activos según los audit logs"""
    query = """
        SELECT
            user_id,
            COUNT(*) as action_count,
            MIN(created_at) as first_action,
            MAX(created_at) as last_action
        FROM audit_logs
        WHERE user_id IS NOT NULL
          AND ($2::timestamp IS NULL OR created_at >= $2)
          AND ($3::timestamp IS NULL OR created_at <= $3)
        GROUP BY user_id
        ORDER BY action_count DESC
        LIMIT $1
    """
    async with pool.acquire() as conn:
        return await conn.fetch(query, limit, start_date, end_date)
