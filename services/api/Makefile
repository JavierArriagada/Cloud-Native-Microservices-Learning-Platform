# =============================================================================
# FastAPI Service - Makefile
# =============================================================================
# Descripción: Comandos para desarrollo del servicio FastAPI
# Modos: Docker (default) y Local (Python local)
# =============================================================================

.PHONY: help
.DEFAULT_GOAL := help

# Variables
SERVICE_NAME := api
PYTHON := python3
PIP := pip3
VENV := venv
DOCKER_COMPOSE := docker compose
COMPOSE_FILE := infrastructure/docker/docker-compose.yml
COMPOSE_DEV := infrastructure/docker/docker-compose.dev.yml

# Colores
RED := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[0;33m
BLUE := \033[0;34m
NC := \033[0m

# =============================================================================
# 📋 AYUDA
# =============================================================================

help: ## Mostrar esta ayuda
	@echo "$(BLUE)═══════════════════════════════════════════════════════════$(NC)"
	@echo "$(GREEN)  FastAPI Service - Comandos de Desarrollo$(NC)"
	@echo "$(BLUE)═══════════════════════════════════════════════════════════$(NC)"
	@echo ""
	@echo "$(YELLOW)Modo Docker (Recomendado):$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		grep -v "LOCAL" | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-25s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(YELLOW)Modo Local (Python local):$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		grep "LOCAL" | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-25s$(NC) %s\n", $$1, $$2}'
	@echo ""

# =============================================================================
# 🐳 MODO DOCKER - DESARROLLO
# =============================================================================

dev: ## [DOCKER] Levantar servicio en modo desarrollo
	@echo "$(GREEN)🐳 Levantando FastAPI en Docker...$(NC)"
	cd ../.. && $(DOCKER_COMPOSE) -f $(COMPOSE_FILE) -f $(COMPOSE_DEV) up -d $(SERVICE_NAME)
	@echo "$(GREEN)✅ FastAPI corriendo en http://localhost/api$(NC)"
	@echo "$(GREEN)📚 Docs en http://localhost/api/docs$(NC)"

stop: ## [DOCKER] Detener servicio
	@echo "$(YELLOW)⏹️  Deteniendo FastAPI...$(NC)"
	cd ../.. && $(DOCKER_COMPOSE) -f $(COMPOSE_FILE) -f $(COMPOSE_DEV) stop $(SERVICE_NAME)

restart: ## [DOCKER] Reiniciar servicio
	@$(MAKE) stop
	@$(MAKE) dev

logs: ## [DOCKER] Ver logs en tiempo real
	cd ../.. && $(DOCKER_COMPOSE) -f $(COMPOSE_FILE) -f $(COMPOSE_DEV) logs -f $(SERVICE_NAME)

logs-tail: ## [DOCKER] Ver últimas 100 líneas de logs
	cd ../.. && $(DOCKER_COMPOSE) -f $(COMPOSE_FILE) -f $(COMPOSE_DEV) logs --tail=100 $(SERVICE_NAME)

shell: ## [DOCKER] Abrir shell en container
	cd ../.. && $(DOCKER_COMPOSE) -f $(COMPOSE_FILE) -f $(COMPOSE_DEV) exec $(SERVICE_NAME) /bin/sh

shell-root: ## [DOCKER] Abrir shell como root
	cd ../.. && $(DOCKER_COMPOSE) -f $(COMPOSE_FILE) -f $(COMPOSE_DEV) exec -u root $(SERVICE_NAME) /bin/sh

build: ## [DOCKER] Build imagen del servicio
	@echo "$(GREEN)🔨 Building FastAPI image...$(NC)"
	cd ../.. && $(DOCKER_COMPOSE) -f $(COMPOSE_FILE) build --no-cache $(SERVICE_NAME)
	@echo "$(GREEN)✅ Build completado$(NC)"

rebuild: ## [DOCKER] Rebuild y reiniciar
	@$(MAKE) build
	@$(MAKE) restart

# =============================================================================
# 🐳 MODO DOCKER - TESTING
# =============================================================================

test: ## [DOCKER] Ejecutar tests
	@echo "$(GREEN)🧪 Ejecutando tests en Docker...$(NC)"
	cd ../.. && $(DOCKER_COMPOSE) -f $(COMPOSE_FILE) run --rm $(SERVICE_NAME) pytest tests/ -v

test-cov: ## [DOCKER] Tests con coverage
	@echo "$(GREEN)📊 Tests con coverage...$(NC)"
	cd ../.. && $(DOCKER_COMPOSE) -f $(COMPOSE_FILE) run --rm $(SERVICE_NAME) pytest --cov=app --cov-report=html --cov-report=term tests/
	@echo "$(GREEN)✅ Coverage report en htmlcov/index.html$(NC)"

test-watch: ## [DOCKER] Tests en modo watch
	cd ../.. && $(DOCKER_COMPOSE) -f $(COMPOSE_FILE) run --rm $(SERVICE_NAME) pytest-watch tests/

test-integration: ## [DOCKER] Solo tests de integración
	cd ../.. && $(DOCKER_COMPOSE) -f $(COMPOSE_FILE) run --rm $(SERVICE_NAME) pytest tests/integration/ -v

test-unit: ## [DOCKER] Solo tests unitarios
	cd ../.. && $(DOCKER_COMPOSE) -f $(COMPOSE_FILE) run --rm $(SERVICE_NAME) pytest tests/unit/ -v

# =============================================================================
# 🐳 MODO DOCKER - CALIDAD DE CÓDIGO
# =============================================================================

lint: ## [DOCKER] Verificar código con ruff y black
	@echo "$(GREEN)🔍 Verificando código...$(NC)"
	cd ../.. && $(DOCKER_COMPOSE) -f $(COMPOSE_FILE) run --rm $(SERVICE_NAME) ruff check .
	cd ../.. && $(DOCKER_COMPOSE) -f $(COMPOSE_FILE) run --rm $(SERVICE_NAME) black --check .

lint-fix: ## [DOCKER] Auto-corregir problemas
	@echo "$(GREEN)🔧 Auto-corrigiendo código...$(NC)"
	cd ../.. && $(DOCKER_COMPOSE) -f $(COMPOSE_FILE) run --rm $(SERVICE_NAME) ruff check --fix .
	cd ../.. && $(DOCKER_COMPOSE) -f $(COMPOSE_FILE) run --rm $(SERVICE_NAME) black .

format: ## [DOCKER] Formatear código con black
	cd ../.. && $(DOCKER_COMPOSE) -f $(COMPOSE_FILE) run --rm $(SERVICE_NAME) black .

type-check: ## [DOCKER] Verificar tipos con mypy
	cd ../.. && $(DOCKER_COMPOSE) -f $(COMPOSE_FILE) run --rm $(SERVICE_NAME) mypy app/

# =============================================================================
# 🐳 MODO DOCKER - DATABASE
# =============================================================================

db-migrate: ## [DOCKER] Ejecutar migraciones
	@echo "$(GREEN)📦 Ejecutando migraciones...$(NC)"
	cd ../.. && $(DOCKER_COMPOSE) -f $(COMPOSE_FILE) exec $(SERVICE_NAME) alembic upgrade head

db-migrate-create: ## [DOCKER] Crear migración (uso: make db-migrate-create MSG="mensaje")
	@echo "$(GREEN)📝 Creando migración...$(NC)"
	cd ../.. && $(DOCKER_COMPOSE) -f $(COMPOSE_FILE) exec $(SERVICE_NAME) alembic revision --autogenerate -m "$(MSG)"

db-migrate-down: ## [DOCKER] Revertir última migración
	cd ../.. && $(DOCKER_COMPOSE) -f $(COMPOSE_FILE) exec $(SERVICE_NAME) alembic downgrade -1

db-migrate-history: ## [DOCKER] Ver historial de migraciones
	cd ../.. && $(DOCKER_COMPOSE) -f $(COMPOSE_FILE) exec $(SERVICE_NAME) alembic history

db-seed: ## [DOCKER] Cargar datos de ejemplo
	@echo "$(GREEN)🌱 Cargando datos de ejemplo...$(NC)"
	cd ../.. && $(DOCKER_COMPOSE) -f $(COMPOSE_FILE) exec $(SERVICE_NAME) python -m scripts.seed_data

# =============================================================================
# 🐍 MODO LOCAL - SETUP
# =============================================================================

local-setup: ## [LOCAL] Configurar entorno local (virtualenv + deps)
	@echo "$(GREEN)🔧 Configurando entorno local...$(NC)"
	@if [ ! -d "$(VENV)" ]; then \
		echo "$(YELLOW)Creando virtualenv...$(NC)"; \
		$(PYTHON) -m venv $(VENV); \
	fi
	@echo "$(YELLOW)Instalando dependencias...$(NC)"
	./$(VENV)/bin/$(PIP) install -r requirements.txt
	./$(VENV)/bin/$(PIP) install -r requirements-dev.txt
	@echo "$(GREEN)✅ Entorno local configurado$(NC)"
	@echo "$(YELLOW)Activar con: source $(VENV)/bin/activate$(NC)"

local-clean: ## [LOCAL] Eliminar virtualenv
	@echo "$(YELLOW)🧹 Eliminando virtualenv...$(NC)"
	rm -rf $(VENV)
	rm -rf __pycache__ .pytest_cache .ruff_cache .mypy_cache htmlcov
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

# =============================================================================
# 🐍 MODO LOCAL - DESARROLLO
# =============================================================================

local-dev: ## [LOCAL] Ejecutar servidor local con hot-reload
	@echo "$(GREEN)🚀 Iniciando FastAPI local...$(NC)"
	@if [ ! -d "$(VENV)" ]; then \
		echo "$(RED)❌ Virtualenv no existe. Ejecuta 'make local-setup' primero$(NC)"; \
		exit 1; \
	fi
	@echo "$(YELLOW)Servidor en http://localhost:8000$(NC)"
	@echo "$(YELLOW)Docs en http://localhost:8000/docs$(NC)"
	./$(VENV)/bin/uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

local-dev-debug: ## [LOCAL] Ejecutar con debugger (puerto 5678)
	@echo "$(GREEN)🐛 Iniciando con debugger...$(NC)"
	./$(VENV)/bin/python -m debugpy --listen 0.0.0.0:5678 --wait-for-client -m uvicorn app.main:app --reload

local-shell: ## [LOCAL] Abrir Python shell interactivo
	./$(VENV)/bin/python

local-ipython: ## [LOCAL] Abrir IPython shell
	@if ! ./$(VENV)/bin/pip show ipython > /dev/null 2>&1; then \
		echo "$(YELLOW)Instalando IPython...$(NC)"; \
		./$(VENV)/bin/$(PIP) install ipython; \
	fi
	./$(VENV)/bin/ipython

# =============================================================================
# 🐍 MODO LOCAL - TESTING
# =============================================================================

local-test: ## [LOCAL] Ejecutar tests localmente
	@echo "$(GREEN)🧪 Ejecutando tests...$(NC)"
	./$(VENV)/bin/pytest tests/ -v

local-test-cov: ## [LOCAL] Tests con coverage
	@echo "$(GREEN)📊 Tests con coverage...$(NC)"
	./$(VENV)/bin/pytest --cov=app --cov-report=html --cov-report=term tests/
	@echo "$(GREEN)✅ Coverage report en htmlcov/index.html$(NC)"

local-test-watch: ## [LOCAL] Tests en modo watch
	./$(VENV)/bin/pytest-watch tests/

local-test-integration: ## [LOCAL] Solo tests de integración
	./$(VENV)/bin/pytest tests/integration/ -v

local-test-unit: ## [LOCAL] Solo tests unitarios
	./$(VENV)/bin/pytest tests/unit/ -v

# =============================================================================
# 🐍 MODO LOCAL - CALIDAD
# =============================================================================

local-lint: ## [LOCAL] Verificar código
	@echo "$(GREEN)🔍 Verificando código...$(NC)"
	./$(VENV)/bin/ruff check .
	./$(VENV)/bin/black --check .

local-lint-fix: ## [LOCAL] Auto-corregir problemas
	@echo "$(GREEN)🔧 Auto-corrigiendo...$(NC)"
	./$(VENV)/bin/ruff check --fix .
	./$(VENV)/bin/black .

local-format: ## [LOCAL] Formatear código
	./$(VENV)/bin/black .

local-type-check: ## [LOCAL] Verificar tipos
	./$(VENV)/bin/mypy app/

# =============================================================================
# 🐍 MODO LOCAL - DATABASE
# =============================================================================

local-db-migrate: ## [LOCAL] Ejecutar migraciones
	@echo "$(GREEN)📦 Ejecutando migraciones...$(NC)"
	./$(VENV)/bin/alembic upgrade head

local-db-migrate-create: ## [LOCAL] Crear migración
	@echo "$(GREEN)📝 Creando migración...$(NC)"
	./$(VENV)/bin/alembic revision --autogenerate -m "$(MSG)"

local-db-migrate-down: ## [LOCAL] Revertir migración
	./$(VENV)/bin/alembic downgrade -1

local-db-migrate-history: ## [LOCAL] Ver historial
	./$(VENV)/bin/alembic history

local-db-seed: ## [LOCAL] Cargar datos de ejemplo
	@echo "$(GREEN)🌱 Cargando datos...$(NC)"
	./$(VENV)/bin/python -m scripts.seed_data

# =============================================================================
# 🔧 UTILIDADES
# =============================================================================

deps-update: ## Actualizar dependencias en requirements.txt
	@echo "$(GREEN)📦 Actualizando dependencias...$(NC)"
	./$(VENV)/bin/$(PIP) list --outdated

deps-install: ## Instalar nueva dependencia (uso: make deps-install PKG=nombre)
	@echo "$(GREEN)📦 Instalando $(PKG)...$(NC)"
	./$(VENV)/bin/$(PIP) install $(PKG)
	./$(VENV)/bin/$(PIP) freeze > requirements.txt

health: ## Verificar health del servicio
	@curl -s http://localhost/api/health | jq . || echo "$(RED)Servicio no responde$(NC)"

health-local: ## Verificar health del servicio local
	@curl -s http://localhost:8000/health | jq . || echo "$(RED)Servicio no responde$(NC)"

# =============================================================================
# 🎯 WORKFLOWS COMPLETOS
# =============================================================================

first-run: local-setup ## Primera ejecución (setup local)
	@echo "$(GREEN)✅ Setup completado$(NC)"
	@echo "$(YELLOW)Siguiente: make local-dev o make dev$(NC)"

ci: ## Simular CI/CD localmente
	@$(MAKE) local-lint
	@$(MAKE) local-test-cov
	@echo "$(GREEN)✅ CI pipeline OK$(NC)"

clean-all: local-clean ## Limpieza completa
	@echo "$(GREEN)✅ Limpieza completada$(NC)"

# =============================================================================
# FIN DEL MAKEFILE
# =============================================================================
