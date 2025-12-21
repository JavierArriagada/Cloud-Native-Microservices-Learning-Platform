"""
Mining Seed Data Script

Script para poblar la base de datos con datos de ejemplo del dominio minero:
- Yacimientos (Deposits)
- Minas (Mines)
- Fases de explotación (Mine Phases)
- Bloques del modelo de bloques (Blocks)
- Coordenadas geoespaciales (Coordinates)
- Mineralogía (Mineralogy)
- Tipos de equipos (Equipment Types)
- Equipos (Equipment)
- Operadores (Operators)
- Reactivos (Reagents)
- Áreas de proceso (Process Areas)

Ejecutar con:
    docker compose exec api python -m scripts.seed_mining_data

O desde Makefile:
    make db-seed-mining
"""

import asyncio
import asyncpg
import os
import sys
import uuid
from datetime import datetime, timedelta
from decimal import Decimal
import random

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.config import settings


# =============================================================================
# DATOS REALISTAS DE MINERÍA CHILENA
# =============================================================================

CHILEAN_DEPOSITS = [
    {
        "code": "DEP-TEND",
        "name": "El Teniente",
        "genetic_model": "Pórfido Cuprífero",
        "primary_commodity": "COPPER",
        "secondary_commodity": "MOLYBDENUM",
        "measured_resources_mt": Decimal("4500.000"),
        "indicated_resources_mt": Decimal("2800.000"),
        "inferred_resources_mt": Decimal("1200.000"),
        "proven_reserves_mt": Decimal("2100.000"),
        "probable_reserves_mt": Decimal("1800.000"),
        "avg_cu_grade_pct": Decimal("0.520"),
        "avg_mo_grade_pct": Decimal("0.0180"),
        "country": "Chile",
        "region": "O'Higgins",
        "province": "Cachapoal",
        "commune": "Machalí",
        "description": "Mayor yacimiento de cobre subterráneo del mundo. Operado por CODELCO.",
        "latitude": Decimal("-34.0892"),
        "longitude": Decimal("-70.3517"),
        "elevation_masl": Decimal("2300.00"),
    },
    {
        "code": "DEP-CHUQ",
        "name": "Chuquicamata",
        "genetic_model": "Pórfido Cuprífero",
        "primary_commodity": "COPPER",
        "secondary_commodity": "MOLYBDENUM",
        "measured_resources_mt": Decimal("6800.000"),
        "indicated_resources_mt": Decimal("3500.000"),
        "inferred_resources_mt": Decimal("2000.000"),
        "proven_reserves_mt": Decimal("3200.000"),
        "probable_reserves_mt": Decimal("2500.000"),
        "avg_cu_grade_pct": Decimal("0.450"),
        "avg_mo_grade_pct": Decimal("0.0210"),
        "country": "Chile",
        "region": "Antofagasta",
        "province": "El Loa",
        "commune": "Calama",
        "description": "Una de las minas a cielo abierto más grandes del mundo. Transición a subterránea.",
        "latitude": Decimal("-22.2990"),
        "longitude": Decimal("-68.9264"),
        "elevation_masl": Decimal("2850.00"),
    },
    {
        "code": "DEP-ESCO",
        "name": "Escondida",
        "genetic_model": "Pórfido Cuprífero",
        "primary_commodity": "COPPER",
        "secondary_commodity": "GOLD",
        "measured_resources_mt": Decimal("12000.000"),
        "indicated_resources_mt": Decimal("5600.000"),
        "inferred_resources_mt": Decimal("3200.000"),
        "proven_reserves_mt": Decimal("4800.000"),
        "probable_reserves_mt": Decimal("3100.000"),
        "avg_cu_grade_pct": Decimal("0.580"),
        "avg_mo_grade_pct": Decimal("0.0050"),
        "country": "Chile",
        "region": "Antofagasta",
        "province": "Antofagasta",
        "commune": "Antofagasta",
        "description": "Mayor productor de cobre del mundo. Operado por BHP.",
        "latitude": Decimal("-24.2667"),
        "longitude": Decimal("-69.0667"),
        "elevation_masl": Decimal("3050.00"),
    },
]

EQUIPMENT_TYPES_DATA = [
    # Equipos de Mina
    {"code": "CAM-797F", "name": "Camión Minero CAT 797F", "category": "HAUL_TRUCK",
     "manufacturer": "Caterpillar", "model": "797F", "capacity": Decimal("400.00"),
     "capacity_unit": "t", "power_kw": Decimal("2983.00"), "expected_life_hours": 60000},
    {"code": "PAL-7495", "name": "Pala Eléctrica CAT 7495", "category": "EXCAVATOR",
     "manufacturer": "Caterpillar", "model": "7495 HF", "capacity": Decimal("75.00"),
     "capacity_unit": "m³", "power_kw": Decimal("4474.00"), "expected_life_hours": 80000},
    {"code": "CAR-994K", "name": "Cargador Frontal CAT 994K", "category": "LOADER",
     "manufacturer": "Caterpillar", "model": "994K", "capacity": Decimal("45.00"),
     "capacity_unit": "t", "power_kw": Decimal("1177.00"), "expected_life_hours": 50000},
    {"code": "PER-D75K", "name": "Perforadora Atlas Copco D75KS", "category": "DRILL",
     "manufacturer": "Atlas Copco", "model": "D75KS", "capacity": Decimal("311.00"),
     "capacity_unit": "mm", "power_kw": Decimal("746.00"), "expected_life_hours": 40000},

    # Equipos de Chancado
    {"code": "CHA-PRIM", "name": "Chancador Primario Giratorio", "category": "CRUSHER",
     "manufacturer": "Metso", "model": "Superior MKIII 60-110", "capacity": Decimal("15000.00"),
     "capacity_unit": "tph", "power_kw": Decimal("750.00"), "expected_life_hours": 100000},
    {"code": "CHA-SECO", "name": "Chancador Secundario Cono", "category": "CRUSHER",
     "manufacturer": "Metso", "model": "MP1000", "capacity": Decimal("3000.00"),
     "capacity_unit": "tph", "power_kw": Decimal("750.00"), "expected_life_hours": 80000},

    # Equipos de Molienda
    {"code": "MOL-SAG", "name": "Molino SAG 40x25", "category": "MILL",
     "manufacturer": "FLSmidth", "model": "SAG 40x25", "capacity": Decimal("5500.00"),
     "capacity_unit": "tph", "power_kw": Decimal("28000.00"), "expected_life_hours": 150000},
    {"code": "MOL-BOL", "name": "Molino de Bolas 24x36", "category": "MILL",
     "manufacturer": "FLSmidth", "model": "BM 24x36", "capacity": Decimal("3200.00"),
     "capacity_unit": "tph", "power_kw": Decimal("18000.00"), "expected_life_hours": 150000},

    # Equipos de Flotación
    {"code": "FLO-RGH", "name": "Celda de Flotación Rougher", "category": "FLOTATION_CELL",
     "manufacturer": "Outotec", "model": "TankCell e630", "capacity": Decimal("630.00"),
     "capacity_unit": "m³", "power_kw": Decimal("500.00"), "expected_life_hours": 80000},
    {"code": "FLO-CLN", "name": "Celda de Flotación Cleaner", "category": "FLOTATION_CELL",
     "manufacturer": "Outotec", "model": "TankCell e300", "capacity": Decimal("300.00"),
     "capacity_unit": "m³", "power_kw": Decimal("250.00"), "expected_life_hours": 80000},

    # Bombas y Transporte
    {"code": "BOM-WAR", "name": "Bomba de Pulpa Warman", "category": "PUMP",
     "manufacturer": "Weir Minerals", "model": "Warman WBH 650", "capacity": Decimal("4500.00"),
     "capacity_unit": "m³/h", "power_kw": Decimal("1500.00"), "expected_life_hours": 20000},
    {"code": "CON-OVL", "name": "Correa Transportadora Overland", "category": "CONVEYOR",
     "manufacturer": "Thyssenkrupp", "model": "Overland 72", "capacity": Decimal("12000.00"),
     "capacity_unit": "tph", "power_kw": Decimal("5000.00"), "expected_life_hours": 100000},

    # Clasificación
    {"code": "CIC-GMA", "name": "Batería de Hidrociclones Gmax", "category": "CYCLONE",
     "manufacturer": "FLSmidth", "model": "Krebs gMAX 33", "capacity": Decimal("2500.00"),
     "capacity_unit": "m³/h", "power_kw": None, "expected_life_hours": 15000},

    # Espesamiento
    {"code": "ESP-HRT", "name": "Espesador de Alta Tasa", "category": "THICKENER",
     "manufacturer": "Outotec", "model": "Thickener HRT 45m", "capacity": Decimal("3500.00"),
     "capacity_unit": "tph", "power_kw": Decimal("150.00"), "expected_life_hours": 200000},

    # Filtración
    {"code": "FIL-PRES", "name": "Filtro Prensa", "category": "FILTER",
     "manufacturer": "Outotec", "model": "Larox PF 96/96", "capacity": Decimal("250.00"),
     "capacity_unit": "tph", "power_kw": Decimal("300.00"), "expected_life_hours": 50000},
]

REAGENTS_DATA = [
    # Colectores
    {"code": "REA-PAX", "name": "Potasio Amil Xantato", "commercial_name": "PAX",
     "reagent_type": "COLLECTOR", "chemical_family": "Xantatos",
     "chemical_formula": "C5H11OCS2K", "molecular_weight": Decimal("202.36"),
     "density": Decimal("1.12"), "recommended_dosage_min": Decimal("15.00"),
     "recommended_dosage_max": Decimal("35.00"), "dosage_unit": "g/t",
     "unit_cost": Decimal("2.50"), "cost_currency": "USD", "cost_unit": "kg",
     "supplier": "Cytec Industries", "hazard_class": "Corrosivo"},
    {"code": "REA-SIPX", "name": "Isopropil Xantato de Sodio", "commercial_name": "SIPX",
     "reagent_type": "COLLECTOR", "chemical_family": "Xantatos",
     "chemical_formula": "C3H7OCS2Na", "molecular_weight": Decimal("158.21"),
     "density": Decimal("1.10"), "recommended_dosage_min": Decimal("10.00"),
     "recommended_dosage_max": Decimal("30.00"), "dosage_unit": "g/t",
     "unit_cost": Decimal("2.20"), "cost_currency": "USD", "cost_unit": "kg",
     "supplier": "BASF", "hazard_class": "Corrosivo"},
    {"code": "REA-3418A", "name": "Aerophine 3418A", "commercial_name": "AP-3418A",
     "reagent_type": "COLLECTOR", "chemical_family": "Ditiofosfatos",
     "chemical_formula": "Proprietary", "molecular_weight": None,
     "density": Decimal("1.08"), "recommended_dosage_min": Decimal("5.00"),
     "recommended_dosage_max": Decimal("20.00"), "dosage_unit": "g/t",
     "unit_cost": Decimal("4.50"), "cost_currency": "USD", "cost_unit": "kg",
     "supplier": "Cytec Industries", "hazard_class": "Irritante"},

    # Espumantes
    {"code": "REA-MIBC", "name": "Metil Isobutil Carbinol", "commercial_name": "MIBC",
     "reagent_type": "FROTHER", "chemical_family": "Alcoholes",
     "chemical_formula": "C6H14O", "molecular_weight": Decimal("102.17"),
     "density": Decimal("0.81"), "recommended_dosage_min": Decimal("15.00"),
     "recommended_dosage_max": Decimal("40.00"), "dosage_unit": "g/t",
     "unit_cost": Decimal("1.80"), "cost_currency": "USD", "cost_unit": "kg",
     "supplier": "Dow Chemical", "hazard_class": "Inflamable"},
    {"code": "REA-DF250", "name": "Dowfroth 250", "commercial_name": "DF-250",
     "reagent_type": "FROTHER", "chemical_family": "Glicoles",
     "chemical_formula": "Polypropylene Glycol", "molecular_weight": Decimal("250.00"),
     "density": Decimal("0.97"), "recommended_dosage_min": Decimal("10.00"),
     "recommended_dosage_max": Decimal("30.00"), "dosage_unit": "g/t",
     "unit_cost": Decimal("2.10"), "cost_currency": "USD", "cost_unit": "kg",
     "supplier": "Dow Chemical", "hazard_class": "Irritante"},

    # Depresantes
    {"code": "REA-NaHS", "name": "Sulfhidrato de Sodio", "commercial_name": "NaHS",
     "reagent_type": "DEPRESSANT", "chemical_family": "Sulfuros",
     "chemical_formula": "NaHS", "molecular_weight": Decimal("56.06"),
     "density": Decimal("1.79"), "recommended_dosage_min": Decimal("500.00"),
     "recommended_dosage_max": Decimal("2000.00"), "dosage_unit": "g/t",
     "unit_cost": Decimal("0.45"), "cost_currency": "USD", "cost_unit": "kg",
     "supplier": "Tessenderlo", "hazard_class": "Tóxico"},
    {"code": "REA-CMC", "name": "Carboximetil Celulosa", "commercial_name": "CMC",
     "reagent_type": "DEPRESSANT", "chemical_family": "Polímeros",
     "chemical_formula": "Polymer", "molecular_weight": None,
     "density": Decimal("1.59"), "recommended_dosage_min": Decimal("50.00"),
     "recommended_dosage_max": Decimal("200.00"), "dosage_unit": "g/t",
     "unit_cost": Decimal("1.20"), "cost_currency": "USD", "cost_unit": "kg",
     "supplier": "Ashland", "hazard_class": "No Peligroso"},

    # Modificadores de pH
    {"code": "REA-CAL", "name": "Cal Hidratada", "commercial_name": "Lime",
     "reagent_type": "PH_MODIFIER", "chemical_family": "Hidróxidos",
     "chemical_formula": "Ca(OH)2", "molecular_weight": Decimal("74.09"),
     "density": Decimal("2.21"), "recommended_dosage_min": Decimal("1000.00"),
     "recommended_dosage_max": Decimal("5000.00"), "dosage_unit": "g/t",
     "unit_cost": Decimal("0.08"), "cost_currency": "USD", "cost_unit": "kg",
     "supplier": "Inacal", "hazard_class": "Irritante"},
    {"code": "REA-H2SO4", "name": "Ácido Sulfúrico", "commercial_name": "H2SO4",
     "reagent_type": "PH_MODIFIER", "chemical_family": "Ácidos",
     "chemical_formula": "H2SO4", "molecular_weight": Decimal("98.08"),
     "density": Decimal("1.84"), "recommended_dosage_min": Decimal("100.00"),
     "recommended_dosage_max": Decimal("500.00"), "dosage_unit": "g/t",
     "unit_cost": Decimal("0.12"), "cost_currency": "USD", "cost_unit": "kg",
     "supplier": "ENAMI", "hazard_class": "Corrosivo"},

    # Activadores
    {"code": "REA-CuSO4", "name": "Sulfato de Cobre", "commercial_name": "CuSO4",
     "reagent_type": "ACTIVATOR", "chemical_family": "Sulfatos",
     "chemical_formula": "CuSO4·5H2O", "molecular_weight": Decimal("249.69"),
     "density": Decimal("2.29"), "recommended_dosage_min": Decimal("50.00"),
     "recommended_dosage_max": Decimal("300.00"), "dosage_unit": "g/t",
     "unit_cost": Decimal("1.50"), "cost_currency": "USD", "cost_unit": "kg",
     "supplier": "Boliden", "hazard_class": "Irritante"},
]

MINERALOGY_DATA = [
    # Minerales de Mena (Cobre)
    {"mineral_name": "Calcopirita", "mineral_formula": "CuFeS2", "mineral_class": "MENA",
     "abundance_pct": Decimal("45.00"), "is_primary_ore": True, "floatability": "HIGH",
     "natural_hydrophobicity": False, "associated_minerals": "Pirita, Bornita, Molibdenita"},
    {"mineral_name": "Bornita", "mineral_formula": "Cu5FeS4", "mineral_class": "MENA",
     "abundance_pct": Decimal("15.00"), "is_primary_ore": True, "floatability": "HIGH",
     "natural_hydrophobicity": False, "associated_minerals": "Calcopirita, Covelina"},
    {"mineral_name": "Calcosita", "mineral_formula": "Cu2S", "mineral_class": "MENA",
     "abundance_pct": Decimal("8.00"), "is_primary_ore": True, "floatability": "MEDIUM",
     "natural_hydrophobicity": False, "associated_minerals": "Bornita, Calcosita"},
    {"mineral_name": "Covelina", "mineral_formula": "CuS", "mineral_class": "MENA",
     "abundance_pct": Decimal("5.00"), "is_primary_ore": True, "floatability": "MEDIUM",
     "natural_hydrophobicity": False, "associated_minerals": "Calcosita, Bornita"},

    # Molibdeno
    {"mineral_name": "Molibdenita", "mineral_formula": "MoS2", "mineral_class": "MENA",
     "abundance_pct": Decimal("2.00"), "is_primary_ore": True, "floatability": "HIGH",
     "natural_hydrophobicity": True, "associated_minerals": "Calcopirita, Pirita"},

    # Ganga
    {"mineral_name": "Pirita", "mineral_formula": "FeS2", "mineral_class": "GANGA",
     "abundance_pct": Decimal("12.00"), "is_primary_ore": False, "floatability": "MEDIUM",
     "natural_hydrophobicity": False, "associated_minerals": "Calcopirita, Arsenopirita",
     "arsenic_content_ppm": Decimal("150.00")},
    {"mineral_name": "Cuarzo", "mineral_formula": "SiO2", "mineral_class": "GANGA",
     "abundance_pct": Decimal("25.00"), "is_primary_ore": False, "floatability": "LOW",
     "natural_hydrophobicity": False, "associated_minerals": "Feldespato, Sericita"},
    {"mineral_name": "Feldespato", "mineral_formula": "KAlSi3O8", "mineral_class": "GANGA",
     "abundance_pct": Decimal("18.00"), "is_primary_ore": False, "floatability": "LOW",
     "natural_hydrophobicity": False, "associated_minerals": "Cuarzo, Biotita"},
    {"mineral_name": "Sericita", "mineral_formula": "KAl2(AlSi3O10)(OH)2", "mineral_class": "ALTERACION",
     "abundance_pct": Decimal("10.00"), "is_primary_ore": False, "floatability": "LOW",
     "natural_hydrophobicity": False, "associated_minerals": "Cuarzo, Caolinita"},
]

PROCESS_AREAS_DATA = [
    {"code": "PA-CRUSH", "name": "Chancado Primario", "area_type": "CRUSHING", "sequence_order": 1,
     "design_capacity": Decimal("15000.00"), "capacity_unit": "tph", "circuit_type": None},
    {"code": "PA-GRIND", "name": "Molienda SAG/Bolas", "area_type": "GRINDING", "sequence_order": 2,
     "design_capacity": Decimal("5500.00"), "capacity_unit": "tph", "circuit_type": None},
    {"code": "PA-ROUGH", "name": "Flotación Rougher", "area_type": "ROUGHER", "sequence_order": 3,
     "design_capacity": Decimal("5500.00"), "capacity_unit": "tph", "target_recovery_pct": Decimal("92.00"),
     "circuit_type": "COLLECTIVE"},
    {"code": "PA-SCAV", "name": "Flotación Scavenger", "area_type": "SCAVENGER", "sequence_order": 4,
     "design_capacity": Decimal("4000.00"), "capacity_unit": "tph", "target_recovery_pct": Decimal("8.00"),
     "circuit_type": "COLLECTIVE"},
    {"code": "PA-CLN1", "name": "Primera Limpieza", "area_type": "CLEANER", "sequence_order": 5,
     "design_capacity": Decimal("800.00"), "capacity_unit": "tph", "target_recovery_pct": Decimal("98.00"),
     "target_grade_pct": Decimal("28.00"), "circuit_type": "COLLECTIVE"},
    {"code": "PA-REGRIND", "name": "Remolienda", "area_type": "REGRIND", "sequence_order": 6,
     "design_capacity": Decimal("400.00"), "capacity_unit": "tph", "circuit_type": None},
    {"code": "PA-CLN2", "name": "Segunda Limpieza", "area_type": "CLEANER", "sequence_order": 7,
     "design_capacity": Decimal("400.00"), "capacity_unit": "tph", "target_recovery_pct": Decimal("99.00"),
     "target_grade_pct": Decimal("32.00"), "circuit_type": "COLLECTIVE"},
    {"code": "PA-SELMO", "name": "Flotación Selectiva Mo", "area_type": "SELECTIVE", "sequence_order": 8,
     "design_capacity": Decimal("150.00"), "capacity_unit": "tph", "target_recovery_pct": Decimal("85.00"),
     "target_grade_pct": Decimal("52.00"), "circuit_type": "SELECTIVE_MO"},
    {"code": "PA-THICK", "name": "Espesamiento", "area_type": "THICKENING", "sequence_order": 9,
     "design_capacity": Decimal("3500.00"), "capacity_unit": "tph", "circuit_type": None},
    {"code": "PA-FILT", "name": "Filtración", "area_type": "FILTRATION", "sequence_order": 10,
     "design_capacity": Decimal("250.00"), "capacity_unit": "tph", "circuit_type": None},
]

OPERATORS_DATA = [
    {"employee_code": "OP-001", "first_name": "Carlos", "last_name": "González Muñoz",
     "email": "cgonzalez@mina.cl", "phone": "+56 9 8765 4321", "job_title": "Operador Pala Eléctrica",
     "department": "Mina", "default_shift": "DAY", "license_number": "LIC-2021-0045"},
    {"employee_code": "OP-002", "first_name": "María", "last_name": "Rodríguez Silva",
     "email": "mrodriguez@mina.cl", "phone": "+56 9 8765 4322", "job_title": "Operador Camión",
     "department": "Mina", "default_shift": "NIGHT", "license_number": "LIC-2020-0123"},
    {"employee_code": "OP-003", "first_name": "Juan", "last_name": "Pérez López",
     "email": "jperez@mina.cl", "phone": "+56 9 8765 4323", "job_title": "Operador Perforadora",
     "department": "Mina", "default_shift": "DAY", "license_number": "LIC-2019-0089"},
    {"employee_code": "OP-004", "first_name": "Ana", "last_name": "Martínez Vega",
     "email": "amartinez@mina.cl", "phone": "+56 9 8765 4324", "job_title": "Operador Sala de Control",
     "department": "Planta", "default_shift": "SWING", "license_number": None},
    {"employee_code": "OP-005", "first_name": "Pedro", "last_name": "Sánchez Díaz",
     "email": "psanchez@mina.cl", "phone": "+56 9 8765 4325", "job_title": "Técnico Metalurgista",
     "department": "Planta", "default_shift": "DAY", "license_number": None},
    {"employee_code": "OP-006", "first_name": "Luis", "last_name": "Hernández Castro",
     "email": "lhernandez@mina.cl", "phone": "+56 9 8765 4326", "job_title": "Mecánico de Equipos",
     "department": "Mantenimiento", "default_shift": "DAY", "license_number": "LIC-MEC-2022-0034"},
    {"employee_code": "OP-007", "first_name": "Carmen", "last_name": "Torres Fuentes",
     "email": "ctorres@mina.cl", "phone": "+56 9 8765 4327", "job_title": "Electricista Industrial",
     "department": "Mantenimiento", "default_shift": "NIGHT", "license_number": "LIC-ELE-2021-0067"},
    {"employee_code": "OP-008", "first_name": "Roberto", "last_name": "Vargas Morales",
     "email": "rvargas@mina.cl", "phone": "+56 9 8765 4328", "job_title": "Supervisor de Turno",
     "department": "Mina", "default_shift": "DAY", "license_number": "LIC-SUP-2018-0012"},
]


# =============================================================================
# FUNCIONES DE SEED
# =============================================================================

async def seed_deposits(conn: asyncpg.Connection) -> dict:
    """Crear yacimientos mineros"""
    print("\n🏔️  Creando yacimientos (deposits)...")

    deposit_ids = {}

    for deposit in CHILEAN_DEPOSITS:
        # Check if exists
        check_query = "SELECT id FROM deposits WHERE code = $1"
        existing = await conn.fetchrow(check_query, deposit["code"])

        if existing:
            print(f"  ℹ️  Yacimiento ya existe: {deposit['name']}")
            deposit_ids[deposit["code"]] = existing["id"]
            continue

        deposit_id = uuid.uuid4()
        deposit_ids[deposit["code"]] = deposit_id

        create_query = """
            INSERT INTO deposits (
                id, code, name, genetic_model, primary_commodity, secondary_commodity,
                measured_resources_mt, indicated_resources_mt, inferred_resources_mt,
                proven_reserves_mt, probable_reserves_mt, avg_cu_grade_pct, avg_mo_grade_pct,
                country, region, province, commune, description
            ) VALUES (
                $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18
            )
        """

        await conn.execute(
            create_query,
            deposit_id,
            deposit["code"],
            deposit["name"],
            deposit["genetic_model"],
            deposit["primary_commodity"],
            deposit["secondary_commodity"],
            deposit["measured_resources_mt"],
            deposit["indicated_resources_mt"],
            deposit["inferred_resources_mt"],
            deposit["proven_reserves_mt"],
            deposit["probable_reserves_mt"],
            deposit["avg_cu_grade_pct"],
            deposit["avg_mo_grade_pct"],
            deposit["country"],
            deposit["region"],
            deposit["province"],
            deposit["commune"],
            deposit["description"],
        )
        print(f"  ✅ Yacimiento creado: {deposit['name']}")

    return deposit_ids


async def seed_coordinates(conn: asyncpg.Connection, deposit_ids: dict):
    """Crear coordenadas geoespaciales"""
    print("\n📍 Creando coordenadas...")

    for deposit in CHILEAN_DEPOSITS:
        deposit_id = deposit_ids.get(deposit["code"])
        if not deposit_id:
            continue

        # Check if exists
        check_query = "SELECT id FROM coordinates WHERE deposit_id = $1 AND point_type = 'CENTROID'"
        existing = await conn.fetchrow(check_query, deposit_id)

        if existing:
            print(f"  ℹ️  Coordenadas ya existen para: {deposit['name']}")
            continue

        create_query = """
            INSERT INTO coordinates (
                id, deposit_id, point_type, latitude, longitude, elevation_masl,
                utm_zone, coordinate_system, datum
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
        """

        await conn.execute(
            create_query,
            uuid.uuid4(),
            deposit_id,
            "CENTROID",
            deposit["latitude"],
            deposit["longitude"],
            deposit["elevation_masl"],
            "19S",  # UTM Zone for Chile
            "WGS84",
            "WGS84",
        )
        print(f"  ✅ Coordenadas creadas para: {deposit['name']}")


async def seed_mineralogy(conn: asyncpg.Connection, deposit_ids: dict):
    """Crear mineralogía"""
    print("\n💎 Creando mineralogía...")

    # Use first deposit for mineralogy
    first_deposit_id = list(deposit_ids.values())[0] if deposit_ids else None
    if not first_deposit_id:
        print("  ⚠️  No hay yacimientos. Saltando mineralogía.")
        return

    for mineral in MINERALOGY_DATA:
        # Check if exists
        check_query = """
            SELECT id FROM mineralogy
            WHERE deposit_id = $1 AND mineral_name = $2
        """
        existing = await conn.fetchrow(check_query, first_deposit_id, mineral["mineral_name"])

        if existing:
            print(f"  ℹ️  Mineral ya existe: {mineral['mineral_name']}")
            continue

        create_query = """
            INSERT INTO mineralogy (
                id, deposit_id, mineral_name, mineral_formula, mineral_class,
                abundance_pct, is_primary_ore, floatability, natural_hydrophobicity,
                associated_minerals, arsenic_content_ppm
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
        """

        await conn.execute(
            create_query,
            uuid.uuid4(),
            first_deposit_id,
            mineral["mineral_name"],
            mineral["mineral_formula"],
            mineral["mineral_class"],
            mineral.get("abundance_pct"),
            mineral["is_primary_ore"],
            mineral.get("floatability"),
            mineral.get("natural_hydrophobicity"),
            mineral.get("associated_minerals"),
            mineral.get("arsenic_content_ppm"),
        )
        print(f"  ✅ Mineral creado: {mineral['mineral_name']}")


async def seed_mines(conn: asyncpg.Connection, deposit_ids: dict) -> dict:
    """Crear minas"""
    print("\n⛏️  Creando minas...")

    mine_ids = {}

    mine_data = [
        {"deposit_code": "DEP-TEND", "code": "MIN-TEND-01", "name": "El Teniente - Mina Principal",
         "mine_type": "UNDERGROUND", "design_capacity_tpd": Decimal("140000.00")},
        {"deposit_code": "DEP-CHUQ", "code": "MIN-CHUQ-01", "name": "Chuquicamata - Rajo Abierto",
         "mine_type": "OPEN_PIT", "design_capacity_tpd": Decimal("180000.00")},
        {"deposit_code": "DEP-CHUQ", "code": "MIN-CHUQ-02", "name": "Chuquicamata Subterránea",
         "mine_type": "UNDERGROUND", "design_capacity_tpd": Decimal("140000.00")},
        {"deposit_code": "DEP-ESCO", "code": "MIN-ESCO-01", "name": "Escondida - Norte",
         "mine_type": "OPEN_PIT", "design_capacity_tpd": Decimal("200000.00")},
    ]

    for mine in mine_data:
        deposit_id = deposit_ids.get(mine["deposit_code"])
        if not deposit_id:
            continue

        # Check if exists
        check_query = "SELECT id FROM mines WHERE code = $1"
        existing = await conn.fetchrow(check_query, mine["code"])

        if existing:
            print(f"  ℹ️  Mina ya existe: {mine['name']}")
            mine_ids[mine["code"]] = existing["id"]
            continue

        mine_id = uuid.uuid4()
        mine_ids[mine["code"]] = mine_id

        create_query = """
            INSERT INTO mines (
                id, deposit_id, code, name, mine_type, design_capacity_tpd,
                current_capacity_tpd, start_date, is_active
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
        """

        await conn.execute(
            create_query,
            mine_id,
            deposit_id,
            mine["code"],
            mine["name"],
            mine["mine_type"],
            mine["design_capacity_tpd"],
            mine["design_capacity_tpd"] * Decimal("0.85"),  # 85% utilization
            datetime.now() - timedelta(days=random.randint(3650, 7300)),  # 10-20 years ago
            True,
        )
        print(f"  ✅ Mina creada: {mine['name']}")

    return mine_ids


async def seed_mine_phases(conn: asyncpg.Connection, mine_ids: dict) -> dict:
    """Crear fases de explotación"""
    print("\n📊 Creando fases de mina...")

    phase_ids = {}

    for mine_code, mine_id in mine_ids.items():
        for phase_num in range(1, 4):  # 3 phases per mine
            phase_code = f"{mine_code}-F{phase_num}"

            # Check if exists
            check_query = "SELECT id FROM mine_phases WHERE code = $1"
            existing = await conn.fetchrow(check_query, phase_code)

            if existing:
                phase_ids[phase_code] = existing["id"]
                continue

            phase_id = uuid.uuid4()
            phase_ids[phase_code] = phase_id

            create_query = """
                INSERT INTO mine_phases (
                    id, mine_id, code, name, sequence_number,
                    design_tonnage_mt, design_cu_grade_pct, design_mo_grade_pct,
                    design_strip_ratio, elevation_top_masl, elevation_bottom_masl,
                    planned_start_date, is_active, is_completed
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14)
            """

            await conn.execute(
                create_query,
                phase_id,
                mine_id,
                phase_code,
                f"Fase {phase_num}",
                phase_num,
                Decimal(str(random.randint(50, 200))),  # 50-200 Mt
                Decimal(str(random.uniform(0.4, 0.8))),  # 0.4-0.8% Cu
                Decimal(str(random.uniform(0.01, 0.03))),  # 0.01-0.03% Mo
                Decimal(str(random.uniform(1.5, 4.0))),  # Strip ratio
                Decimal(str(random.randint(3000, 3500))),
                Decimal(str(random.randint(2500, 3000))),
                datetime.now() + timedelta(days=365 * phase_num),
                phase_num == 1,  # Only first phase is active
                False,
            )
        print(f"  ✅ Fases creadas para: {mine_code}")

    return phase_ids


async def seed_blocks(conn: asyncpg.Connection, phase_ids: dict):
    """Crear bloques del modelo de bloques (muestra pequeña)"""
    print("\n🧱 Creando bloques de modelo...")

    # Create a small sample of blocks for first phase only
    first_phase_id = list(phase_ids.values())[0] if phase_ids else None
    if not first_phase_id:
        print("  ⚠️  No hay fases. Saltando bloques.")
        return

    # Check existing blocks
    check_query = "SELECT COUNT(*) as count FROM blocks WHERE mine_phase_id = $1"
    result = await conn.fetchrow(check_query, first_phase_id)

    if result["count"] > 0:
        print(f"  ℹ️  Ya existen {result['count']} bloques")
        return

    # Create 5x5x3 = 75 sample blocks
    block_count = 0
    for i in range(5):
        for j in range(5):
            for k in range(3):
                block_code = f"BLK-{i:02d}{j:02d}{k:02d}"

                # Random mineral type
                mineral_types = ["SULFIDE", "OXIDE", "MIXED", "TRANSITION"]
                mineral_type = random.choice(mineral_types)

                create_query = """
                    INSERT INTO blocks (
                        id, mine_phase_id, code, block_i, block_j, block_k,
                        centroid_x, centroid_y, centroid_z,
                        size_x, size_y, size_z, tonnage, density,
                        cu_grade_pct, mo_grade_pct, mineral_type, is_mined
                    ) VALUES (
                        $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18
                    )
                """

                await conn.execute(
                    create_query,
                    uuid.uuid4(),
                    first_phase_id,
                    block_code,
                    i, j, k,
                    Decimal(str(1000 + i * 10)),  # centroid_x
                    Decimal(str(2000 + j * 10)),  # centroid_y
                    Decimal(str(3000 - k * 15)),  # centroid_z
                    Decimal("10.00"),  # size_x
                    Decimal("10.00"),  # size_y
                    Decimal("15.00"),  # size_z
                    Decimal(str(random.randint(3000, 5000))),  # tonnage
                    Decimal(str(random.uniform(2.5, 2.8))),  # density
                    Decimal(str(random.uniform(0.3, 1.0))),  # cu_grade
                    Decimal(str(random.uniform(0.005, 0.03))),  # mo_grade
                    mineral_type,
                    False,
                )
                block_count += 1

    print(f"  ✅ {block_count} bloques creados")


async def seed_equipment_types(conn: asyncpg.Connection) -> dict:
    """Crear tipos de equipos"""
    print("\n🔧 Creando tipos de equipos...")

    type_ids = {}

    for eq_type in EQUIPMENT_TYPES_DATA:
        # Check if exists
        check_query = "SELECT id FROM equipment_types WHERE code = $1"
        existing = await conn.fetchrow(check_query, eq_type["code"])

        if existing:
            type_ids[eq_type["code"]] = existing["id"]
            continue

        type_id = uuid.uuid4()
        type_ids[eq_type["code"]] = type_id

        create_query = """
            INSERT INTO equipment_types (
                id, code, name, category, manufacturer, model,
                capacity, capacity_unit, power_kw, expected_life_hours, is_active
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
        """

        await conn.execute(
            create_query,
            type_id,
            eq_type["code"],
            eq_type["name"],
            eq_type["category"],
            eq_type["manufacturer"],
            eq_type["model"],
            eq_type["capacity"],
            eq_type["capacity_unit"],
            eq_type.get("power_kw"),
            eq_type["expected_life_hours"],
            True,
        )
        print(f"  ✅ Tipo de equipo: {eq_type['name']}")

    return type_ids


async def seed_equipment(conn: asyncpg.Connection, mine_ids: dict, type_ids: dict):
    """Crear equipos"""
    print("\n🚜 Creando equipos...")

    if not mine_ids or not type_ids:
        print("  ⚠️  No hay minas o tipos de equipo. Saltando.")
        return

    first_mine_id = list(mine_ids.values())[0]

    equipment_list = [
        ("CAM-797F", "EQ-CAM-001", "Camión #001", "Mina"),
        ("CAM-797F", "EQ-CAM-002", "Camión #002", "Mina"),
        ("CAM-797F", "EQ-CAM-003", "Camión #003", "Mina"),
        ("PAL-7495", "EQ-PAL-001", "Pala Eléctrica #001", "Mina"),
        ("CAR-994K", "EQ-CAR-001", "Cargador #001", "Mina"),
        ("PER-D75K", "EQ-PER-001", "Perforadora #001", "Mina"),
        ("CHA-PRIM", "EQ-CHP-001", "Chancador Primario #001", "Chancado"),
        ("MOL-SAG", "EQ-SAG-001", "Molino SAG #001", "Molienda"),
        ("MOL-BOL", "EQ-BOL-001", "Molino de Bolas #001", "Molienda"),
        ("FLO-RGH", "EQ-FLR-001", "Celda Rougher #001", "Flotación"),
        ("FLO-CLN", "EQ-FLC-001", "Celda Cleaner #001", "Flotación"),
        ("BOM-WAR", "EQ-BOM-001", "Bomba de Pulpa #001", "Transporte"),
    ]

    for type_code, eq_code, eq_name, location in equipment_list:
        type_id = type_ids.get(type_code)
        if not type_id:
            continue

        # Check if exists
        check_query = "SELECT id FROM equipment WHERE code = $1"
        existing = await conn.fetchrow(check_query, eq_code)

        if existing:
            continue

        create_query = """
            INSERT INTO equipment (
                id, equipment_type_id, mine_id, code, name, serial_number,
                status, location_area, installation_date, total_operating_hours, is_active
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
        """

        await conn.execute(
            create_query,
            uuid.uuid4(),
            type_id,
            first_mine_id,
            eq_code,
            eq_name,
            f"SN-{random.randint(100000, 999999)}",
            "OPERATIONAL",
            location,
            datetime.now() - timedelta(days=random.randint(365, 1825)),
            Decimal(str(random.randint(10000, 50000))),
            True,
        )
        print(f"  ✅ Equipo: {eq_name}")


async def seed_operators(conn: asyncpg.Connection, mine_ids: dict):
    """Crear operadores"""
    print("\n👷 Creando operadores...")

    if not mine_ids:
        print("  ⚠️  No hay minas. Saltando operadores.")
        return

    first_mine_id = list(mine_ids.values())[0]

    for operator in OPERATORS_DATA:
        # Check if exists
        check_query = "SELECT id FROM operators WHERE employee_code = $1"
        existing = await conn.fetchrow(check_query, operator["employee_code"])

        if existing:
            continue

        create_query = """
            INSERT INTO operators (
                id, mine_id, employee_code, first_name, last_name,
                email, phone, job_title, department, default_shift,
                license_number, hire_date, is_active
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13)
        """

        await conn.execute(
            create_query,
            uuid.uuid4(),
            first_mine_id,
            operator["employee_code"],
            operator["first_name"],
            operator["last_name"],
            operator.get("email"),
            operator.get("phone"),
            operator["job_title"],
            operator.get("department"),
            operator.get("default_shift"),
            operator.get("license_number"),
            datetime.now() - timedelta(days=random.randint(365, 3650)),
            True,
        )
        print(f"  ✅ Operador: {operator['first_name']} {operator['last_name']}")


async def seed_reagents(conn: asyncpg.Connection):
    """Crear reactivos químicos"""
    print("\n🧪 Creando reactivos...")

    for reagent in REAGENTS_DATA:
        # Check if exists
        check_query = "SELECT id FROM reagents WHERE code = $1"
        existing = await conn.fetchrow(check_query, reagent["code"])

        if existing:
            continue

        create_query = """
            INSERT INTO reagents (
                id, code, name, commercial_name, reagent_type, chemical_family,
                chemical_formula, molecular_weight, density,
                recommended_dosage_min, recommended_dosage_max, dosage_unit,
                unit_cost, cost_currency, cost_unit, supplier, hazard_class, is_active
            ) VALUES (
                $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18
            )
        """

        await conn.execute(
            create_query,
            uuid.uuid4(),
            reagent["code"],
            reagent["name"],
            reagent.get("commercial_name"),
            reagent["reagent_type"],
            reagent.get("chemical_family"),
            reagent.get("chemical_formula"),
            reagent.get("molecular_weight"),
            reagent.get("density"),
            reagent.get("recommended_dosage_min"),
            reagent.get("recommended_dosage_max"),
            reagent.get("dosage_unit"),
            reagent.get("unit_cost"),
            reagent.get("cost_currency"),
            reagent.get("cost_unit"),
            reagent.get("supplier"),
            reagent.get("hazard_class"),
            True,
        )
        print(f"  ✅ Reactivo: {reagent['name']}")


async def seed_process_areas(conn: asyncpg.Connection, mine_ids: dict):
    """Crear áreas de proceso"""
    print("\n🏭 Creando áreas de proceso...")

    if not mine_ids:
        print("  ⚠️  No hay minas. Saltando áreas de proceso.")
        return

    first_mine_id = list(mine_ids.values())[0]

    for area in PROCESS_AREAS_DATA:
        # Check if exists
        check_query = "SELECT id FROM process_areas WHERE code = $1 AND mine_id = $2"
        existing = await conn.fetchrow(check_query, area["code"], first_mine_id)

        if existing:
            continue

        create_query = """
            INSERT INTO process_areas (
                id, mine_id, code, name, area_type, sequence_order,
                design_capacity, capacity_unit, target_recovery_pct,
                target_grade_pct, circuit_type, is_active
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
        """

        await conn.execute(
            create_query,
            uuid.uuid4(),
            first_mine_id,
            area["code"],
            area["name"],
            area["area_type"],
            area["sequence_order"],
            area.get("design_capacity"),
            area.get("capacity_unit"),
            area.get("target_recovery_pct"),
            area.get("target_grade_pct"),
            area.get("circuit_type"),
            True,
        )
        print(f"  ✅ Área de proceso: {area['name']}")


async def main():
    """Main function"""
    print("=" * 70)
    print("  🏔️  SEED MINING DATA - Entidades Maestras Capa 1")
    print("=" * 70)
    print()

    # Connect to database
    try:
        print("📡 Conectando a base de datos...")
        conn = await asyncpg.connect(settings.get_db_url_asyncpg())
        print("✅ Conexión establecida")

        # Seed data in order (respecting foreign keys)
        deposit_ids = await seed_deposits(conn)
        await seed_coordinates(conn, deposit_ids)
        await seed_mineralogy(conn, deposit_ids)
        mine_ids = await seed_mines(conn, deposit_ids)
        phase_ids = await seed_mine_phases(conn, mine_ids)
        await seed_blocks(conn, phase_ids)
        type_ids = await seed_equipment_types(conn)
        await seed_equipment(conn, mine_ids, type_ids)
        await seed_operators(conn, mine_ids)
        await seed_reagents(conn)
        await seed_process_areas(conn, mine_ids)

        print()
        print("=" * 70)
        print("  ✅ Seed mining data completado exitosamente")
        print("=" * 70)
        print()
        print("📊 Resumen de datos creados:")
        print(f"   - Yacimientos:      {len(CHILEAN_DEPOSITS)}")
        print(f"   - Minas:            {len(mine_ids)}")
        print(f"   - Fases:            {len(phase_ids)}")
        print(f"   - Tipos de equipo:  {len(EQUIPMENT_TYPES_DATA)}")
        print(f"   - Operadores:       {len(OPERATORS_DATA)}")
        print(f"   - Reactivos:        {len(REAGENTS_DATA)}")
        print(f"   - Áreas de proceso: {len(PROCESS_AREAS_DATA)}")
        print()

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        if conn:
            await conn.close()
            print("📡 Conexión cerrada")


if __name__ == "__main__":
    asyncio.run(main())
