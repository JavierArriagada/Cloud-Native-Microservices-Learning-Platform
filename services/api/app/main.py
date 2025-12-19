"""
FastAPI Application - Main Entry Point
Cloud-Native Microservices Learning Platform
"""
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import asyncpg
from datetime import datetime
import os

from app.config import settings
from app.database import get_db_pool, close_db_pool

# =============================================================================
# APPLICATION INITIALIZATION
# =============================================================================

app = FastAPI(
    title="Cloud-Native Microservices Learning Platform API",
    description="RESTful API built with FastAPI, PostgreSQL, and asyncpg",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# =============================================================================
# MIDDLEWARE
# =============================================================================

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =============================================================================
# STARTUP & SHUTDOWN EVENTS
# =============================================================================

@app.on_event("startup")
async def startup_event():
    """Initialize resources on startup"""
    print("🚀 Starting FastAPI application...")
    print(f"📊 Environment: {settings.ENVIRONMENT}")
    print(f"🔍 Debug mode: {settings.DEBUG}")
    # Database pool will be created on first request
    print("✅ Application started successfully")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup resources on shutdown"""
    print("👋 Shutting down application...")
    await close_db_pool()
    print("✅ Application shutdown complete")

# =============================================================================
# HEALTH CHECK ENDPOINTS
# =============================================================================

@app.get("/health", tags=["Health"])
async def health_check():
    """
    Basic health check endpoint
    Returns 200 if service is running
    """
    return {
        "status": "healthy",
        "service": "api",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat(),
    }


@app.get("/ready", tags=["Health"])
async def readiness_check(pool: asyncpg.Pool = Depends(get_db_pool)):
    """
    Readiness check endpoint
    Verifies database connectivity
    """
    try:
        # Test database connection
        async with pool.acquire() as conn:
            version = await conn.fetchval("SELECT version()")

        return {
            "status": "ready",
            "service": "api",
            "database": "connected",
            "postgres_version": version.split()[1] if version else "unknown",
            "timestamp": datetime.utcnow().isoformat(),
        }
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={
                "status": "not_ready",
                "service": "api",
                "database": "disconnected",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat(),
            }
        )


@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint
    """
    return {
        "message": "Welcome to Cloud-Native Microservices Learning Platform API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health",
        "ready": "/ready",
    }

# =============================================================================
# METRICS ENDPOINT (for Prometheus)
# =============================================================================

@app.get("/metrics", tags=["Monitoring"])
async def metrics():
    """
    Prometheus metrics endpoint
    TODO: Implement proper prometheus client metrics
    """
    return {
        "message": "Metrics endpoint - TODO: implement prometheus_client",
        "note": "Install prometheus-fastapi-instrumentator for full metrics"
    }

# =============================================================================
# API V1 ROUTES
# =============================================================================

# TODO: Import and include routers here
# from app.routers import items
# app.include_router(items.router, prefix="/v1", tags=["items"])

@app.get("/v1/items", tags=["Items"])
async def get_items(pool: asyncpg.Pool = Depends(get_db_pool)):
    """
    Example endpoint to list items
    TODO: Implement proper CRUD with database
    """
    try:
        async with pool.acquire() as conn:
            # Example query - will fail if table doesn't exist yet
            # This is just a placeholder
            pass

        # Return mock data for now
        return {
            "items": [
                {"id": 1, "name": "Sample Item 1", "description": "This is a sample"},
                {"id": 2, "name": "Sample Item 2", "description": "Another sample"},
            ],
            "total": 2,
            "note": "Mock data - implement real database queries"
        }
    except Exception as e:
        return {
            "items": [],
            "total": 0,
            "note": "Database not initialized yet - run migrations"
        }

# =============================================================================
# ERROR HANDLERS
# =============================================================================

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Global exception handler
    """
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc) if settings.DEBUG else "An error occurred",
            "timestamp": datetime.utcnow().isoformat(),
        }
    )
