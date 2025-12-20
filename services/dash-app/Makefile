# =============================================================================
# Dash App Service - Makefile
# =============================================================================
# Descripción: Comandos para desarrollo del servicio Dash (Python Dashboard)
# Modos: Docker (default) y Local (Python local)
# =============================================================================

.PHONY: help
.DEFAULT_GOAL := help

# Variables
SERVICE_NAME := dash
PYTHON := python3
PIP := pip3
VENV := venv
DOCKER_COMPOSE := docker compose
COMPOSE_FILE := ../../infrastructure/docker/docker-compose.yml
COMPOSE_DEV := ../../infrastructure/docker/docker-compose.dev.yml

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
	@echo "$(GREEN)  Dash App Service - Comandos de Desarrollo$(NC)"
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
	@echo "$(GREEN)🐳 Levantando Dash App en Docker...$(NC)"
	cd ../.. && $(DOCKER_COMPOSE) -f $(COMPOSE_FILE) -f $(COMPOSE_DEV) up -d $(SERVICE_NAME)
	@echo "$(GREEN)✅ Dash App corriendo en http://localhost/dash$(NC)"

stop: ## [DOCKER] Detener servicio
	@echo "$(YELLOW)⏹️  Deteniendo Dash App...$(NC)"
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
	@echo "$(GREEN)🔨 Building Dash App image...$(NC)"
	cd ../.. && $(DOCKER_COMPOSE) -f $(COMPOSE_FILE) build --no-cache $(SERVICE_NAME)
	@echo "$(GREEN)✅ Build completado$(NC)"

rebuild: ## [DOCKER] Rebuild y reiniciar
	@$(MAKE) build
	@$(MAKE) restart

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
	@echo "$(GREEN)✅ Entorno local configurado$(NC)"
	@echo "$(YELLOW)Activar con: source $(VENV)/bin/activate$(NC)"

local-clean: ## [LOCAL] Eliminar virtualenv
	@echo "$(YELLOW)🧹 Eliminando virtualenv...$(NC)"
	rm -rf $(VENV)
	rm -rf __pycache__ .ruff_cache
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

# =============================================================================
# 🐍 MODO LOCAL - DESARROLLO
# =============================================================================

local-dev: ## [LOCAL] Ejecutar servidor local con hot-reload
	@echo "$(GREEN)🚀 Iniciando Dash App local...$(NC)"
	@if [ ! -d "$(VENV)" ]; then \
		echo "$(RED)❌ Virtualenv no existe. Ejecuta 'make local-setup' primero$(NC)"; \
		exit 1; \
	fi
	@echo "$(YELLOW)Servidor en http://localhost:8050$(NC)"
	./$(VENV)/bin/python app/main.py

local-dev-debug: ## [LOCAL] Ejecutar con debug mode activado
	@echo "$(GREEN)🐛 Iniciando con debug...$(NC)"
	DASH_DEBUG=true ./$(VENV)/bin/python app/main.py

local-shell: ## [LOCAL] Abrir Python shell interactivo
	./$(VENV)/bin/python

local-ipython: ## [LOCAL] Abrir IPython shell
	@if ! ./$(VENV)/bin/pip show ipython > /dev/null 2>&1; then \
		echo "$(YELLOW)Instalando IPython...$(NC)"; \
		./$(VENV)/bin/$(PIP) install ipython; \
	fi
	./$(VENV)/bin/ipython

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
	@curl -s http://localhost/dash | head -n 1 || echo "$(RED)Servicio no responde$(NC)"

health-local: ## Verificar health del servicio local
	@curl -s http://localhost:8050 | head -n 1 || echo "$(RED)Servicio no responde$(NC)"

# =============================================================================
# 🎯 WORKFLOWS COMPLETOS
# =============================================================================

first-run: local-setup ## Primera ejecución (setup local)
	@echo "$(GREEN)✅ Setup completado$(NC)"
	@echo "$(YELLOW)Siguiente: make local-dev o make dev$(NC)"

ci: ## Simular CI/CD localmente
	@$(MAKE) local-lint
	@echo "$(GREEN)✅ CI pipeline OK$(NC)"

clean-all: local-clean ## Limpieza completa
	@echo "$(GREEN)✅ Limpieza completada$(NC)"

# =============================================================================
# FIN DEL MAKEFILE
# =============================================================================
