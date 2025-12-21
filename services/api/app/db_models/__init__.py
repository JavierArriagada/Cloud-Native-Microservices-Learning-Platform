"""
SQLAlchemy Database Models

IMPORTANTE: Estos modelos se usan EXCLUSIVAMENTE para Alembic autogenerate.
NO se deben usar como ORM en runtime.

Para queries, usar SQL puro con asyncpg (ver app/database.py).
"""

from sqlalchemy.orm import declarative_base

# Base para todos los modelos
Base = declarative_base()

# ============================================================================
# Sistema de Usuarios y Autenticación
# ============================================================================
from .user import User
from .role import Role
from .user_role import UserRole
from .session import Session
from .audit_log import AuditLog, AuditAction

# ============================================================================
# Dominio Minero - ENUMs
# ============================================================================
from .mining_enums import (
    MineTypeEnum,
    MineralTypeEnum,
    ProcessAreaTypeEnum,
    EquipmentCategoryEnum,
    EquipmentStatusEnum,
    MaintenanceTypeEnum,
    WorkOrderPriorityEnum,
    WorkOrderStatusEnum,
    ShiftTypeEnum,
    SensorTypeEnum,
    ConcentrateTypeEnum,
)

# ============================================================================
# Capa 1: Entidades Maestras - Yacimientos y Minas
# ============================================================================
from .deposit import Deposit
from .mine import Mine
from .mine_phase import MinePhase
from .block import Block
from .coordinate import Coordinate
from .mineralogy import Mineralogy

# ============================================================================
# Capa 1: Entidades Maestras - Equipos y Operadores
# ============================================================================
from .equipment_type import EquipmentType
from .equipment import Equipment
from .operator import Operator

# ============================================================================
# Capa 1: Entidades Maestras - Proceso
# ============================================================================
from .reagent import Reagent
from .process_area import ProcessArea

# Metadata para Alembic
metadata = Base.metadata

__all__ = [
    # Base
    "Base",
    "metadata",
    # Sistema de Usuarios
    "User",
    "Role",
    "UserRole",
    "Session",
    "AuditLog",
    "AuditAction",
    # ENUMs de Minería
    "MineTypeEnum",
    "MineralTypeEnum",
    "ProcessAreaTypeEnum",
    "EquipmentCategoryEnum",
    "EquipmentStatusEnum",
    "MaintenanceTypeEnum",
    "WorkOrderPriorityEnum",
    "WorkOrderStatusEnum",
    "ShiftTypeEnum",
    "SensorTypeEnum",
    "ConcentrateTypeEnum",
    # Entidades Maestras - Yacimientos
    "Deposit",
    "Mine",
    "MinePhase",
    "Block",
    "Coordinate",
    "Mineralogy",
    # Entidades Maestras - Equipos
    "EquipmentType",
    "Equipment",
    "Operator",
    # Entidades Maestras - Proceso
    "Reagent",
    "ProcessArea",
]
