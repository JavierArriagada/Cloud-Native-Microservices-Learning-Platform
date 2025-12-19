"""
Database Connection Module
Manages PostgreSQL connection pool using asyncpg
"""
import asyncpg
from typing import Optional
from app.config import settings

# Global connection pool
_pool: Optional[asyncpg.Pool] = None


async def get_db_pool() -> asyncpg.Pool:
    """
    Get or create database connection pool
    This function is used as a FastAPI dependency
    """
    global _pool

    if _pool is None:
        print("📦 Creating database connection pool...")
        try:
            _pool = await asyncpg.create_pool(
                dsn=settings.get_db_url_asyncpg(),
                min_size=settings.DB_MIN_POOL_SIZE,
                max_size=settings.DB_MAX_POOL_SIZE,
                timeout=settings.DB_POOL_TIMEOUT,
                command_timeout=60,
                max_queries=50000,
                max_inactive_connection_lifetime=300,
            )
            print(f"✅ Database pool created (min={settings.DB_MIN_POOL_SIZE}, max={settings.DB_MAX_POOL_SIZE})")
        except Exception as e:
            print(f"❌ Failed to create database pool: {e}")
            raise

    return _pool


async def close_db_pool():
    """
    Close database connection pool
    Called on application shutdown
    """
    global _pool

    if _pool is not None:
        print("📦 Closing database connection pool...")
        await _pool.close()
        _pool = None
        print("✅ Database pool closed")


async def execute_query(query: str, *args):
    """
    Execute a query that doesn't return results (INSERT, UPDATE, DELETE)

    Args:
        query: SQL query string
        *args: Query parameters

    Returns:
        Result status
    """
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        result = await conn.execute(query, *args)
        return result


async def fetch_one(query: str, *args):
    """
    Fetch a single row

    Args:
        query: SQL query string
        *args: Query parameters

    Returns:
        Single record or None
    """
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        result = await conn.fetchrow(query, *args)
        return result


async def fetch_all(query: str, *args):
    """
    Fetch multiple rows

    Args:
        query: SQL query string
        *args: Query parameters

    Returns:
        List of records
    """
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        result = await conn.fetch(query, *args)
        return result


async def fetch_val(query: str, *args):
    """
    Fetch a single value

    Args:
        query: SQL query string
        *args: Query parameters

    Returns:
        Single value
    """
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        result = await conn.fetchval(query, *args)
        return result
