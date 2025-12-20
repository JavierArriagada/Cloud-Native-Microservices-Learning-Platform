#!/usr/bin/env python3
"""
Code Generation Scripts

Herramientas para automatizar la generación de código:
- Pydantic schemas desde SQLAlchemy models
- Queries SQL básicas desde SQLAlchemy models
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Type
import inspect

# Add the app directory to the Python path
sys.path.insert(0, str(Path(__file__).parent / "app"))

from sqlalchemy.ext.declarative import DeclarativeMeta
from pydantic import BaseModel, Field
from pydantic_sqlalchemy import sqlalchemy_to_pydantic
import importlib.util


def load_sqlalchemy_models() -> Dict[str, Type[DeclarativeMeta]]:
    """Cargar todos los modelos SQLAlchemy desde db_models"""
    models = {}

    # Importar el módulo db_models
    spec = importlib.util.spec_from_file_location(
        "db_models",
        Path(__file__).parent / "app" / "db_models" / "__init__.py"
    )
    db_models_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(db_models_module)

    # Encontrar todas las clases que heredan de Base
    for name, obj in inspect.getmembers(db_models_module):
        if (inspect.isclass(obj) and
            hasattr(obj, '__tablename__') and
            name != 'Base'):
            models[name.lower()] = obj

    return models


def generate_pydantic_schemas(model_name: str, sqlalchemy_model: Type[DeclarativeMeta]) -> str:
    """Generar schemas Pydantic desde un modelo SQLAlchemy"""

    # Convertir a Pydantic usando pydantic-sqlalchemy
    PydanticModel = sqlalchemy_to_pydantic(sqlalchemy_model)

    # Crear schemas adicionales
    base_fields = {}
    for column in sqlalchemy_model.__table__.columns:
        field_name = column.name
        field_type = str(column.type).split('(')[0].lower()  # e.g., 'varchar' -> 'str'

        # Mapear tipos SQL a Python
        type_mapping = {
            'uuid': 'UUID',
            'varchar': 'str',
            'text': 'str',
            'integer': 'int',
            'numeric': 'Decimal',
            'boolean': 'bool',
            'timestamp': 'datetime',
            'date': 'date',
        }

        python_type = type_mapping.get(field_type, 'str')

        # Agregar importaciones necesarias
        imports = set()
        if python_type == 'UUID':
            imports.add('from uuid import UUID')
        elif python_type == 'Decimal':
            imports.add('from decimal import Decimal')
        elif python_type == 'datetime':
            imports.add('from datetime import datetime')

        base_fields[field_name] = python_type

    # Generar el código
    code_lines = [
        '"""',
        f'{model_name.title()} Pydantic Schemas',
        '',
        f'Schemas para validación de requests/responses relacionados con {model_name}.',
        'GENERADO AUTOMÁTICAMENTE - NO EDITAR MANUALMENTE',
        '"""',
        '',
        'from datetime import datetime',
        'from typing import Optional',
        'from uuid import UUID',
        'from decimal import Decimal',
        'from pydantic import BaseModel, Field',
        '',
        '',
        '# Base Schema',
        f'class {model_name.title()}Base(BaseModel):',
        '    """Schema base con campos comunes"""',
    ]

    # Agregar campos base (excluyendo auditoría)
    for field_name, field_type in base_fields.items():
        if field_name not in ['id', 'created_at', 'updated_at']:
            if field_name.endswith('_id'):
                # Foreign keys como opcionales
                code_lines.append(f'    {field_name}: Optional[UUID] = None')
            else:
                # Campos normales
                nullable = 'Optional[' if field_name in ['description'] else ''
                end_optional = ']' if nullable else ''
                code_lines.append(f'    {field_name}: {nullable}{field_type}{end_optional}')

    code_lines.extend([
        '',
        '',
        '# Create Schema (Request)',
        f'class {model_name.title()}Create({model_name.title()}Base):',
        '    """Schema para crear (POST request)"""',
        '    pass',
        '',
        '',
        '# Update Schema (Request)',
        f'class {model_name.title()}Update(BaseModel):',
        '    """Schema para actualizar (PUT/PATCH request)"""',
    ])

    # Campos de update (todos opcionales)
    for field_name, field_type in base_fields.items():
        if field_name not in ['id', 'created_at', 'updated_at']:
            code_lines.append(f'    {field_name}: Optional[{field_type}] = None')

    code_lines.extend([
        '',
        '',
        '# Database Schema (Internal)',
        f'class {model_name.title()}InDB({model_name.title()}Base):',
        '    """Schema con todos los campos de la DB (uso interno)"""',
        '    id: UUID',
        '    created_at: datetime',
        '    updated_at: datetime',
        '',
        '    model_config = {"from_attributes": True}',
        '',
        '',
        '# Public Schema (Response)',
        f'class {model_name.title()}Public({model_name.title()}Base):',
        '    """Schema público (response API)"""',
        '    id: UUID',
        '    created_at: datetime',
        '',
        '    model_config = {"from_attributes": True}',
    ])

    return '\n'.join(code_lines)


def generate_sql_queries(model_name: str, sqlalchemy_model: Type[DeclarativeMeta]) -> str:
    """Generar queries SQL básicas desde un modelo SQLAlchemy"""

    table_name = sqlalchemy_model.__tablename__
    columns = [col.name for col in sqlalchemy_model.__table__.columns]
    pk_column = next((col.name for col in columns if col == 'id'), 'id')

    code_lines = [
        '"""',
        f'{model_name.title()} SQL Queries',
        '',
        f'Queries SQL puras para operaciones CRUD de {model_name}.',
        'GENERADO AUTOMÁTICAMENTE - NO EDITAR MANUALMENTE',
        '"""',
        '',
        'from typing import Optional',
        'from uuid import UUID',
        'from decimal import Decimal',
        'import asyncpg',
        '',
        '',
        '# ============================================================================',
        '# READ QUERIES',
        '# ============================================================================',
        '',
        f'async def get_{model_name}_by_id(pool: asyncpg.Pool, {model_name}_id: UUID) -> Optional[asyncpg.Record]:',
        f'    """Obtener {model_name} por ID"""',
        f'    query = """',
        f'        SELECT',
    ]

    # Agregar columnas al SELECT
    for col in columns:
        code_lines.append(f'            {col},')

    code_lines.extend([
        f'        FROM {table_name}',
        f'        WHERE id = $1',
        f'    """',
        f'    async with pool.acquire() as conn:',
        f'        return await conn.fetchrow(query, {model_name}_id)',
        '',
        '',
        f'async def get_all_{model_name}s(',
        f'    pool: asyncpg.Pool,',
        f'    limit: int = 100,',
        f'    offset: int = 0',
        f') -> list[asyncpg.Record]:',
        f'    """Obtener lista de {model_name}s con paginación"""',
        f'    query = """',
        f'        SELECT',
    ])

    # Columnas para lista (excluir campos largos)
    list_columns = [col for col in columns if col not in ['description', 'updated_at']]
    for col in list_columns:
        code_lines.append(f'            {col},')

    code_lines.extend([
        f'        FROM {table_name}',
        f'        ORDER BY created_at DESC',
        f'        LIMIT $1 OFFSET $2',
        f'    """',
        f'    async with pool.acquire() as conn:',
        f'        return await conn.fetch(query, limit, offset)',
        '',
        '',
        '# ============================================================================',
        '# CREATE QUERIES',
        '# ============================================================================',
        '',
        f'async def create_{model_name}(',
        f'    pool: asyncpg.Pool,',
    ])

    # Parámetros para create (excluir id, created_at, updated_at)
    create_params = [col for col in columns if col not in ['id', 'created_at', 'updated_at']]
    for param in create_params:
        if param.endswith('_id'):
            code_lines.append(f'    {param}: Optional[UUID] = None,')
        else:
            code_lines.append(f'    {param}: str,')  # Simplificar tipos

    code_lines.extend([
        f') -> asyncpg.Record:',
        f'    """Crear nuevo {model_name}"""',
        f'    query = """',
        f'        INSERT INTO {table_name} (',
    ])

    # Columnas para INSERT
    insert_columns = create_params
    for col in insert_columns[:-1]:
        code_lines.append(f'            {col},')
    code_lines.append(f'            {insert_columns[-1]}')
    code_lines.append(f'        )')
    code_lines.append(f'        VALUES (')

    # Placeholders
    placeholders = [f'${i+1}' for i in range(len(insert_columns))]
    for ph in placeholders[:-1]:
        code_lines.append(f'            {ph},')
    code_lines.append(f'            {placeholders[-1]}')
    code_lines.append(f'        )')
    code_lines.append(f'        RETURNING')

    # RETURNING columns
    for col in columns:
        code_lines.append(f'            {col},')

    code_lines.extend([
        f'    """',
        f'    async with pool.acquire() as conn:',
        f'        return await conn.fetchrow(',
        f'            query,',
    ])

    # Parámetros para execute
    for param in create_params:
        code_lines.append(f'            {param},')

    code_lines.extend([
        f'        )',
        '',
        '',
        '# ============================================================================',
        '# UPDATE QUERIES',
        '# ============================================================================',
        '',
        f'async def update_{model_name}(',
        f'    pool: asyncpg.Pool,',
        f'    {model_name}_id: UUID,',
    ])

    # Parámetros de update (todos opcionales)
    for param in create_params:
        code_lines.append(f'    {param}: Optional[str] = None,')

    code_lines.extend([
        f') -> Optional[asyncpg.Record]:',
        f'    """Actualizar {model_name}"""',
        f'    query = """',
        f'        UPDATE {table_name}',
        f'        SET',
    ])

    # SET clause con COALESCE
    set_parts = []
    for i, param in enumerate(create_params):
        set_parts.append(f'            {param} = COALESCE(${i+2}, {param})')

    for part in set_parts[:-1]:
        code_lines.append(f'{part},')
    code_lines.append(f'{set_parts[-1]},')
    code_lines.append(f'            updated_at = NOW()')
    code_lines.append(f'        WHERE id = $1')
    code_lines.append(f'        RETURNING')

    # RETURNING
    for col in columns:
        code_lines.append(f'            {col},')

    code_lines.extend([
        f'    """',
        f'    async with pool.acquire() as conn:',
        f'        return await conn.fetchrow(',
        f'            query,',
        f'            {model_name}_id,',
    ])

    for param in create_params:
        code_lines.append(f'            {param},')

    code_lines.extend([
        f'        )',
        '',
        '',
        '# ============================================================================',
        '# DELETE QUERIES',
        '# ============================================================================',
        '',
        f'async def delete_{model_name}(pool: asyncpg.Pool, {model_name}_id: UUID) -> bool:',
        f'    """Eliminar {model_name} (hard delete)"""',
        f'    query = """',
        f'        DELETE FROM {table_name}',
        f'        WHERE id = $1',
        f'        RETURNING id',
        f'    """',
        f'    async with pool.acquire() as conn:',
        f'        result = await conn.fetchrow(query, {model_name}_id)',
        f'        return result is not None',
    ])

    return '\n'.join(code_lines)


def main():
    """Generar código automáticamente desde modelos SQLAlchemy"""

    if len(sys.argv) < 2:
        print("Uso: python generate_code.py <model_name>")
        print("Ejemplo: python generate_code.py product")
        sys.exit(1)

    model_name = sys.argv[1].lower()

    # Cargar modelos
    try:
        models = load_sqlalchemy_models()
    except Exception as e:
        print(f"Error cargando modelos: {e}")
        sys.exit(1)

    if model_name not in models:
        print(f"Modelo '{model_name}' no encontrado. Modelos disponibles:")
        for name in models.keys():
            print(f"  - {name}")
        sys.exit(1)

    sqlalchemy_model = models[model_name]

    # Directorios de salida
    models_dir = Path(__file__).parent / "app" / "models"
    queries_dir = Path(__file__).parent / "app" / "queries"

    models_dir.mkdir(exist_ok=True)
    queries_dir.mkdir(exist_ok=True)

    # Generar Pydantic schemas
    pydantic_code = generate_pydantic_schemas(model_name, sqlalchemy_model)
    pydantic_file = models_dir / f"{model_name}.py"

    with open(pydantic_file, 'w', encoding='utf-8') as f:
        f.write(pydantic_code)

    print(f"✅ Generado: {pydantic_file}")

    # Generar queries SQL
    queries_code = generate_sql_queries(model_name, sqlalchemy_model)
    queries_file = queries_dir / f"{model_name}.py"

    with open(queries_file, 'w', encoding='utf-8') as f:
        f.write(queries_code)

    print(f"✅ Generado: {queries_file}")

    print("\n🎉 ¡Código generado exitosamente!")
    print(f"Recuerda actualizar los __init__.py para importar las nuevas clases.")


if __name__ == "__main__":
    main()