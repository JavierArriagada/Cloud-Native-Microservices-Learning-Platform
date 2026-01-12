#!/bin/bash

# =============================================================================
# Script de Instalación Automatizada
# Cloud-Native Microservices Learning Platform
# =============================================================================
# Este script automatiza el proceso de instalación del proyecto
# =============================================================================

set -e  # Salir si hay algún error

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funciones de utilidad
print_header() {
    echo -e "\n${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}\n"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# Verificar si un comando existe
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Banner de bienvenida
clear
echo "
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   🚀 Cloud-Native Microservices Learning Platform            ║
║   Script de Instalación Automatizada                         ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
"

# =============================================================================
# PASO 1: Verificar requisitos previos
# =============================================================================
print_header "Paso 1: Verificando requisitos previos"

# Verificar Docker
if command_exists docker; then
    DOCKER_VERSION=$(docker --version | grep -oP '\d+\.\d+\.\d+' | head -1)
    print_success "Docker instalado (versión $DOCKER_VERSION)"
else
    print_error "Docker NO está instalado"
    echo "Por favor instala Docker Desktop desde: https://www.docker.com/products/docker-desktop"
    exit 1
fi

# Verificar Docker Compose
if command_exists docker && docker compose version >/dev/null 2>&1; then
    COMPOSE_VERSION=$(docker compose version | grep -oP '\d+\.\d+\.\d+' | head -1)
    print_success "Docker Compose instalado (versión $COMPOSE_VERSION)"
else
    print_error "Docker Compose NO está instalado o es una versión antigua"
    echo "Por favor actualiza Docker Desktop para obtener Docker Compose v2"
    exit 1
fi

# Verificar que Docker esté corriendo
if docker info >/dev/null 2>&1; then
    print_success "Docker daemon está corriendo"
else
    print_error "Docker daemon NO está corriendo"
    echo "Por favor inicia Docker Desktop y ejecuta este script nuevamente"
    exit 1
fi

# Verificar Git
if command_exists git; then
    GIT_VERSION=$(git --version | grep -oP '\d+\.\d+\.\d+')
    print_success "Git instalado (versión $GIT_VERSION)"
else
    print_warning "Git NO está instalado (opcional para desarrollo)"
fi

# Verificar Make
if command_exists make; then
    print_success "Make instalado (comandos Makefile disponibles)"
    HAS_MAKE=true
else
    print_warning "Make NO está instalado (se usarán comandos docker compose directos)"
    HAS_MAKE=false
fi

sleep 2

# =============================================================================
# PASO 2: Configurar variables de entorno
# =============================================================================
print_header "Paso 2: Configurando variables de entorno"

if [ -f .env ]; then
    print_warning "El archivo .env ya existe"
    read -p "¿Deseas sobrescribirlo? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        cp .env.example .env
        print_success "Archivo .env creado desde .env.example"
    else
        print_info "Usando el archivo .env existente"
    fi
else
    cp .env.example .env
    print_success "Archivo .env creado desde .env.example"
fi

sleep 1

# =============================================================================
# PASO 3: Verificar puertos disponibles
# =============================================================================
print_header "Paso 3: Verificando puertos disponibles"

PORTS_TO_CHECK=(80 8080 5432 3001 9090)
PORTS_IN_USE=()

for port in "${PORTS_TO_CHECK[@]}"; do
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1 || netstat -an 2>/dev/null | grep ":$port " | grep LISTEN >/dev/null; then
        PORTS_IN_USE+=($port)
        print_warning "Puerto $port está en uso"
    else
        print_success "Puerto $port disponible"
    fi
done

if [ ${#PORTS_IN_USE[@]} -gt 0 ]; then
    print_warning "Algunos puertos están en uso: ${PORTS_IN_USE[*]}"
    print_info "Puedes cambiar los puertos en el archivo .env si hay conflictos"
    read -p "¿Deseas continuar de todos modos? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_error "Instalación cancelada"
        exit 1
    fi
fi

sleep 1

# =============================================================================
# PASO 4: Construir imágenes Docker
# =============================================================================
print_header "Paso 4: Construyendo imágenes Docker"

print_info "Esto puede tomar varios minutos la primera vez..."
echo

if [ "$HAS_MAKE" = true ]; then
    make build
else
    docker compose -f infrastructure/docker/docker-compose.yml -f infrastructure/docker/docker-compose.dev.yml build
fi

if [ $? -eq 0 ]; then
    print_success "Imágenes Docker construidas exitosamente"
else
    print_error "Error al construir las imágenes Docker"
    exit 1
fi

sleep 1

# =============================================================================
# PASO 5: Levantar servicios
# =============================================================================
print_header "Paso 5: Levantando servicios"

if [ "$HAS_MAKE" = true ]; then
    make dev-up
else
    docker compose -f infrastructure/docker/docker-compose.yml -f infrastructure/docker/docker-compose.dev.yml up -d
fi

if [ $? -eq 0 ]; then
    print_success "Servicios levantados exitosamente"
else
    print_error "Error al levantar los servicios"
    exit 1
fi

print_info "Esperando a que los servicios estén listos..."
sleep 15

# =============================================================================
# PASO 6: Verificar estado de los servicios
# =============================================================================
print_header "Paso 6: Verificando estado de los servicios"

if [ "$HAS_MAKE" = true ]; then
    make dev-status
else
    docker compose -f infrastructure/docker/docker-compose.yml -f infrastructure/docker/docker-compose.dev.yml ps
fi

sleep 2

# =============================================================================
# PASO 7: Aplicar migraciones de base de datos
# =============================================================================
print_header "Paso 7: Aplicando migraciones de base de datos"

print_info "Esperando a que PostgreSQL esté listo..."
sleep 10

# Intentar conectar a PostgreSQL
MAX_RETRIES=30
RETRY_COUNT=0
until docker exec mlp-postgres-1 pg_isready -U mlp_user >/dev/null 2>&1 || [ $RETRY_COUNT -eq $MAX_RETRIES ]; do
    print_info "Esperando a PostgreSQL... (intento $((RETRY_COUNT+1))/$MAX_RETRIES)"
    sleep 2
    RETRY_COUNT=$((RETRY_COUNT+1))
done

if [ $RETRY_COUNT -eq $MAX_RETRIES ]; then
    print_error "PostgreSQL no está respondiendo después de $MAX_RETRIES intentos"
    print_info "Puedes intentar ejecutar las migraciones manualmente más tarde con:"
    print_info "  docker exec -it mlp-api-1 python -m alembic upgrade head"
else
    print_success "PostgreSQL está listo"

    # Aplicar migraciones
    print_info "Aplicando migraciones..."
    if docker exec mlp-api-1 python -m alembic upgrade head; then
        print_success "Migraciones aplicadas exitosamente"
    else
        print_warning "Error al aplicar migraciones (puedes intentar manualmente después)"
    fi
fi

sleep 1

# =============================================================================
# PASO 8: Cargar datos de ejemplo
# =============================================================================
print_header "Paso 8: Cargando datos de ejemplo"

read -p "¿Deseas cargar datos de ejemplo? (Y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Nn]$ ]]; then
    print_info "Cargando datos básicos..."
    if docker exec mlp-api-1 python -m scripts.seed_data 2>/dev/null; then
        print_success "Datos básicos cargados"
    else
        print_warning "No se pudieron cargar los datos (el script puede no existir aún)"
    fi

    print_info "Cargando datos de minería..."
    if docker exec mlp-api-1 python -m scripts.seed_mining_data 2>/dev/null; then
        print_success "Datos de minería cargados"
    else
        print_warning "No se pudieron cargar los datos de minería (el script puede no existir aún)"
    fi
else
    print_info "Omitiendo carga de datos de ejemplo"
fi

sleep 1

# =============================================================================
# PASO 9: Verificar instalación
# =============================================================================
print_header "Paso 9: Verificando instalación"

print_info "Probando conectividad de servicios..."
sleep 3

# Test del API
if curl -f -s http://localhost/api/health >/dev/null 2>&1; then
    print_success "API responde correctamente"
else
    print_warning "API no responde (puede necesitar más tiempo para iniciar)"
fi

# Test de Traefik
if curl -f -s http://localhost:8080 >/dev/null 2>&1; then
    print_success "Traefik Dashboard accesible"
else
    print_warning "Traefik Dashboard no responde"
fi

sleep 1

# =============================================================================
# Resumen final
# =============================================================================
clear
print_header "✅ Instalación Completada"

echo "
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   🎉 ¡Instalación exitosa!                                   ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝

📍 ACCESO A SERVICIOS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🌐 Frontend React:       http://localhost
📚 API Docs (Swagger):   http://localhost/api/docs
📊 Dash Dashboard:       http://localhost/dash
🔀 Traefik Dashboard:    http://localhost:8080
📈 Grafana:              http://localhost:3001
   └─ Credenciales:      admin / admin_change_in_production
🔥 Prometheus:           http://localhost:9090

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📖 DOCUMENTACIÓN:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

• Guía completa:         docs/GUIA_INSTALACION.md
• Base de datos:         docs/DATABASE_GUIDE.md
• Workflow desarrollo:   docs/CLAUDE_CODE_WORKFLOW.md
• Credenciales:          docs/DEVELOPMENT_CREDENTIALS.md

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🛠️  COMANDOS ÚTILES:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"

if [ "$HAS_MAKE" = true ]; then
    echo "
• Ver logs:              make dev-logs
• Detener servicios:     make dev-down
• Reiniciar servicios:   make dev-restart
• Estado de servicios:   make dev-status
• Ver todos comandos:    make help
"
else
    echo "
• Ver logs:              docker compose -f infrastructure/docker/docker-compose.yml -f infrastructure/docker/docker-compose.dev.yml logs -f
• Detener servicios:     docker compose -f infrastructure/docker/docker-compose.yml -f infrastructure/docker/docker-compose.dev.yml down
• Estado de servicios:   docker compose -f infrastructure/docker/docker-compose.yml -f infrastructure/docker/docker-compose.dev.yml ps
"
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"

print_success "La plataforma está lista para usar"
print_info "Abre tu navegador en http://localhost para comenzar"

echo ""
