#!/bin/bash
# =============================================================================
# Script Automatizado: Crear Nueva Tabla en Base de Datos
# =============================================================================
# Descripción: Guía interactiva paso a paso para crear una nueva tabla
# Uso: ./scripts/create_table.sh
# =============================================================================

set -e

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Variables
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
DB_MODELS_DIR="$PROJECT_ROOT/app/db_models"
MODELS_DIR="$PROJECT_ROOT/app/models"
QUERIES_DIR="$PROJECT_ROOT/app/queries"

# =============================================================================
# Funciones de Utilidad
# =============================================================================

print_header() {
    echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}  $1${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
    echo ""
}

print_step() {
    echo -e "${CYAN}📝 $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${MAGENTA}ℹ️  $1${NC}"
}

# =============================================================================
# Main Script
# =============================================================================

print_header "🚀 Workflow: Crear Nueva Tabla"

echo -e "${YELLOW}Este script te guiará paso a paso para crear una nueva tabla:${NC}"
echo "  1. Recopilar información"
echo "  2. Crear modelo SQLAlchemy"
echo "  3. Generar migración de Alembic"
echo "  4. Aplicar migración"
echo "  5. Generar Pydantic schemas y queries SQL"
echo "  6. Actualizar imports"
echo "  7. Verificar en base de datos"
echo ""

# =============================================================================
# Paso 1: Recopilar Información
# =============================================================================

print_step "Paso 1: Recopilando información..."
echo ""

read -p "Nombre de la tabla (singular, ej: product, category, order): " TABLE_NAME
TABLE_NAME=$(echo "$TABLE_NAME" | tr '[:upper:]' '[:lower:]' | tr -d ' ')

read -p "Nombre plural de la tabla (ej: products, categories, orders): " TABLE_NAME_PLURAL
TABLE_NAME_PLURAL=$(echo "$TABLE_NAME_PLURAL" | tr '[:upper:]' '[:lower:]' | tr -d ' ')

read -p "Descripción breve de la tabla: " TABLE_DESCRIPTION

read -p "Mensaje de migración (ej: add products table): " MIGRATION_MSG

# Capitalizar para nombre de clase
CLASS_NAME=$(echo "$TABLE_NAME" | sed 's/^./\U&/; s/_\(.\)/\U\1/g')

echo ""
print_info "Resumen:"
echo "  - Tabla: $TABLE_NAME_PLURAL"
echo "  - Clase: $CLASS_NAME"
echo "  - Descripción: $TABLE_DESCRIPTION"
echo "  - Migración: $MIGRATION_MSG"
echo ""

read -p "¿Continuar? [y/N]: " CONFIRM
if [ "$CONFIRM" != "y" ]; then
    print_error "Operación cancelada"
    exit 1
fi

# =============================================================================
# Paso 2: Crear Modelo SQLAlchemy (Template Básico)
# =============================================================================

print_step "Paso 2: Creando template de modelo SQLAlchemy..."
echo ""

MODEL_FILE="$DB_MODELS_DIR/${TABLE_NAME}.py"

if [ -f "$MODEL_FILE" ]; then
    print_warning "El modelo ya existe: $MODEL_FILE"
    read -p "¿Sobrescribir? [y/N]: " OVERWRITE
    if [ "$OVERWRITE" != "y" ]; then
        print_info "Usando modelo existente"
    else
        rm "$MODEL_FILE"
    fi
fi

if [ ! -f "$MODEL_FILE" ]; then
    cat > "$MODEL_FILE" << EOF
"""
$CLASS_NAME SQLAlchemy Model (SOLO PARA ALEMBIC)

Este modelo NO se usa en runtime. Solo sirve para que Alembic
pueda autogenerar migraciones.

$TABLE_DESCRIPTION
"""

from sqlalchemy import (
    Column,
    String,
    Boolean,
    Integer,
    Text,
    DateTime,
    ForeignKey,
    Index,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from . import Base


class $CLASS_NAME(Base):
    """Modelo SQLAlchemy de $CLASS_NAME (solo para Alembic)"""

    __tablename__ = "$TABLE_NAME_PLURAL"

    # Identificación
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # TODO: Agregar tus columnas aquí
    # Ejemplo:
    # name = Column(String(255), nullable=False)
    # description = Column(Text, nullable=True)
    # is_active = Column(Boolean, nullable=False, default=True, server_default="true")

    # Auditoría
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now()
    )

    # Índices y constraints
    __table_args__ = (
        # TODO: Agregar índices aquí
        # Index("idx_${TABLE_NAME_PLURAL}_name", "name"),
        {
            "comment": "$TABLE_DESCRIPTION"
        }
    )
EOF
    print_success "Template creado: $MODEL_FILE"
else
    print_info "Usando modelo existente"
fi

echo ""
print_warning "⚠️  IMPORTANTE: Edita el modelo para agregar tus columnas"
print_info "Archivo: $MODEL_FILE"
echo ""
read -p "Presiona ENTER cuando hayas editado el modelo..."

# =============================================================================
# Paso 3: Actualizar __init__.py de db_models
# =============================================================================

print_step "Paso 3: Actualizando __init__.py de db_models..."
echo ""

INIT_FILE="$DB_MODELS_DIR/__init__.py"

# Verificar si ya está importado
if grep -q "from .${TABLE_NAME} import ${CLASS_NAME}" "$INIT_FILE"; then
    print_info "El modelo ya está importado en __init__.py"
else
    # Agregar import antes de la línea "# Metadata para Alembic"
    sed -i "/# Metadata para Alembic/i from .${TABLE_NAME} import ${CLASS_NAME}" "$INIT_FILE"

    # Agregar a __all__ antes del último ]
    sed -i "/__all__ = \[/,/\]/ s/\]/    \"${CLASS_NAME}\",\n]/" "$INIT_FILE"

    print_success "Modelo importado en __init__.py"
fi

# =============================================================================
# Paso 4: Generar Migración
# =============================================================================

print_step "Paso 4: Generando migración de Alembic..."
echo ""

cd "$PROJECT_ROOT/../.."

# Generar migración
docker compose exec api alembic revision --autogenerate -m "$MIGRATION_MSG"

print_success "Migración generada"
echo ""
print_warning "⚠️  Revisa el archivo de migración en:"
print_info "services/api/alembic/versions/"
echo ""
read -p "¿Migración correcta? [y/N]: " MIGRATION_OK

if [ "$MIGRATION_OK" != "y" ]; then
    print_error "Por favor corrige la migración y vuelve a ejecutar el script"
    exit 1
fi

# =============================================================================
# Paso 5: Aplicar Migración
# =============================================================================

print_step "Paso 5: Aplicando migración..."
echo ""

docker compose exec api alembic upgrade head

print_success "Migración aplicada"

# =============================================================================
# Paso 6: Generar Pydantic Schemas y Queries
# =============================================================================

print_step "Paso 6: Generando Pydantic schemas y queries SQL..."
echo ""

docker compose exec api python -m scripts.generate_code "$TABLE_NAME"

print_success "Código generado"
print_info "Archivos creados:"
echo "  - $MODELS_DIR/${TABLE_NAME}.py"
echo "  - $QUERIES_DIR/${TABLE_NAME}.py"

# =============================================================================
# Paso 7: Actualizar __init__.py de models y queries
# =============================================================================

print_step "Paso 7: Actualizando __init__.py de models y queries..."
echo ""

# TODO: Automatizar esto también
print_warning "⚠️  Actualiza manualmente los siguientes archivos:"
echo "  1. $MODELS_DIR/__init__.py"
echo "  2. $QUERIES_DIR/__init__.py"
echo ""
read -p "Presiona ENTER cuando hayas actualizado los imports..."

# =============================================================================
# Paso 8: Verificar en Base de Datos
# =============================================================================

print_step "Paso 8: Verificando en base de datos..."
echo ""

docker compose exec postgres psql -U mlp_user -d mlp_db -c "\d $TABLE_NAME_PLURAL"

print_success "Tabla verificada"

# =============================================================================
# Paso 9: Seed Data (Opcional)
# =============================================================================

echo ""
read -p "¿Quieres agregar seed data para esta tabla? [y/N]: " ADD_SEED

if [ "$ADD_SEED" = "y" ]; then
    print_step "Paso 9: Agregando seed data..."
    echo ""
    print_warning "⚠️  Edita el archivo: services/api/scripts/seed_data.py"
    print_info "Agrega una función async seed_${TABLE_NAME_PLURAL}(conn) y llámala en main()"
    echo ""
    read -p "Presiona ENTER cuando hayas agregado el seed data..."

    docker compose exec api python -m scripts.seed_data
    print_success "Seed data ejecutado"
fi

# =============================================================================
# Finalización
# =============================================================================

echo ""
print_header "✅ ¡Tabla Creada Exitosamente!"

echo -e "${GREEN}Resumen:${NC}"
echo "  ✅ Modelo SQLAlchemy creado: $MODEL_FILE"
echo "  ✅ Migración aplicada: $MIGRATION_MSG"
echo "  ✅ Pydantic schemas generados: $MODELS_DIR/${TABLE_NAME}.py"
echo "  ✅ Queries SQL generadas: $QUERIES_DIR/${TABLE_NAME}.py"
echo "  ✅ Tabla verificada en base de datos: $TABLE_NAME_PLURAL"
echo ""

echo -e "${YELLOW}📋 Próximos pasos:${NC}"
echo "  1. Revisar y ajustar el modelo SQLAlchemy si es necesario"
echo "  2. Revisar Pydantic schemas generados"
echo "  3. Revisar queries SQL generadas"
echo "  4. Agregar seed data (si no lo hiciste)"
echo "  5. Hacer commit de los cambios"
echo ""

echo -e "${BLUE}Archivos a commitear:${NC}"
echo "  git add services/api/app/db_models/${TABLE_NAME}.py"
echo "  git add services/api/app/db_models/__init__.py"
echo "  git add services/api/app/models/${TABLE_NAME}.py"
echo "  git add services/api/app/queries/${TABLE_NAME}.py"
echo "  git add services/api/alembic/versions/*_${MIGRATION_MSG// /_}.py"
echo "  git commit -m 'feat(db): $MIGRATION_MSG'"
echo ""

print_success "¡Listo! 🎉"
