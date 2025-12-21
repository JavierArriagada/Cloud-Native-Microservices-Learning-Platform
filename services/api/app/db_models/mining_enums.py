"""
Mining Domain ENUMs (SOLO PARA ALEMBIC)

Enumeraciones para el dominio minero de Cu/Mo.
"""
import enum


class MineTypeEnum(str, enum.Enum):
    """Tipos de explotación minera"""
    OPEN_PIT = "OPEN_PIT"
    UNDERGROUND = "UNDERGROUND"
    MIXED = "MIXED"


class MineralTypeEnum(str, enum.Enum):
    """Tipos de mineral según oxidación"""
    SULFIDE = "SULFIDE"
    OXIDE = "OXIDE"
    MIXED = "MIXED"
    TRANSITION = "TRANSITION"


class ProcessAreaTypeEnum(str, enum.Enum):
    """Áreas de proceso de la planta concentradora"""
    CRUSHING = "CRUSHING"
    GRINDING = "GRINDING"
    ROUGHER = "ROUGHER"
    CLEANER = "CLEANER"
    SCAVENGER = "SCAVENGER"
    REGRIND = "REGRIND"
    SELECTIVE = "SELECTIVE"
    THICKENING = "THICKENING"
    FILTRATION = "FILTRATION"


class EquipmentCategoryEnum(str, enum.Enum):
    """Categorías de equipos mineros"""
    HAUL_TRUCK = "HAUL_TRUCK"
    EXCAVATOR = "EXCAVATOR"
    LOADER = "LOADER"
    DRILL = "DRILL"
    CRUSHER = "CRUSHER"
    MILL = "MILL"
    FLOTATION_CELL = "FLOTATION_CELL"
    PUMP = "PUMP"
    CONVEYOR = "CONVEYOR"
    CYCLONE = "CYCLONE"
    THICKENER = "THICKENER"
    FILTER = "FILTER"


class EquipmentStatusEnum(str, enum.Enum):
    """Estados operativos de equipos"""
    OPERATIONAL = "OPERATIONAL"
    MAINTENANCE = "MAINTENANCE"
    FAILED = "FAILED"
    STANDBY = "STANDBY"
    DECOMMISSIONED = "DECOMMISSIONED"


class MaintenanceTypeEnum(str, enum.Enum):
    """Tipos de mantenimiento según ISO 14224"""
    PREVENTIVE = "PREVENTIVE"
    CORRECTIVE = "CORRECTIVE"
    PREDICTIVE = "PREDICTIVE"
    EMERGENCY = "EMERGENCY"
    SCHEDULED = "SCHEDULED"


class WorkOrderPriorityEnum(str, enum.Enum):
    """Prioridades de órdenes de trabajo"""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class WorkOrderStatusEnum(str, enum.Enum):
    """Estados de órdenes de trabajo"""
    PENDING = "PENDING"
    SCHEDULED = "SCHEDULED"
    IN_PROGRESS = "IN_PROGRESS"
    ON_HOLD = "ON_HOLD"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class ShiftTypeEnum(str, enum.Enum):
    """Turnos de operación"""
    DAY = "DAY"
    NIGHT = "NIGHT"
    SWING = "SWING"


class SensorTypeEnum(str, enum.Enum):
    """Tipos de sensores industriales"""
    FLOW = "FLOW"
    PRESSURE = "PRESSURE"
    TEMPERATURE = "TEMPERATURE"
    LEVEL = "LEVEL"
    PH = "PH"
    ORP = "ORP"
    DENSITY = "DENSITY"
    VIBRATION = "VIBRATION"
    POWER = "POWER"
    SPEED = "SPEED"
    WEIGHT = "WEIGHT"
    PARTICLE_SIZE = "PARTICLE_SIZE"


class ConcentrateTypeEnum(str, enum.Enum):
    """Tipos de concentrado producido"""
    COPPER = "COPPER"
    MOLYBDENUM = "MOLYBDENUM"
    COLLECTIVE = "COLLECTIVE"
