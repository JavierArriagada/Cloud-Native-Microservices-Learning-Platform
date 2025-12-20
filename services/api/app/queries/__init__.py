"""
SQL Queries Package

Este paquete contiene queries SQL puras organizadas por entidad.
NO usar ORM - todas las queries son SQL puro ejecutado con asyncpg.
"""

from . import users
from . import roles
from . import sessions
from . import auth

__all__ = [
    "users",
    "roles",
    "sessions",
    "auth",
]
