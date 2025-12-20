# =============================================================================
# React App Service - Makefile
# =============================================================================
# Descripción: Comandos para desarrollo del servicio React + TypeScript
# Modos: Docker (default) y Local (Node.js local)
# =============================================================================

.PHONY: help
.DEFAULT_GOAL := help

# Variables
SERVICE_NAME := react
NODE := node
NPM := npm
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
	@echo "$(GREEN)  React App Service - Comandos de Desarrollo$(NC)"
	@echo "$(BLUE)═══════════════════════════════════════════════════════════$(NC)"
	@echo ""
	@echo "$(YELLOW)Modo Docker (Recomendado):$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		grep -v "LOCAL" | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-25s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(YELLOW)Modo Local (Node.js local):$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		grep "LOCAL" | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-25s$(NC) %s\n", $$1, $$2}'
	@echo ""

# =============================================================================
# 🐳 MODO DOCKER - DESARROLLO
# =============================================================================

dev: ## [DOCKER] Levantar servicio en modo desarrollo
	@echo "$(GREEN)🐳 Levantando React App en Docker...$(NC)"
	cd ../.. && $(DOCKER_COMPOSE) -f $(COMPOSE_FILE) -f $(COMPOSE_DEV) up -d $(SERVICE_NAME)
	@echo "$(GREEN)✅ React App corriendo en http://localhost$(NC)"

stop: ## [DOCKER] Detener servicio
	@echo "$(YELLOW)⏹️  Deteniendo React App...$(NC)"
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
	@echo "$(GREEN)🔨 Building React App image...$(NC)"
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
	cd ../.. && $(DOCKER_COMPOSE) -f $(COMPOSE_FILE) run --rm $(SERVICE_NAME) npm test -- --run

test-watch: ## [DOCKER] Tests en modo watch
	cd ../.. && $(DOCKER_COMPOSE) -f $(COMPOSE_FILE) run --rm $(SERVICE_NAME) npm test

test-coverage: ## [DOCKER] Tests con coverage
	@echo "$(GREEN)📊 Tests con coverage...$(NC)"
	cd ../.. && $(DOCKER_COMPOSE) -f $(COMPOSE_FILE) run --rm $(SERVICE_NAME) npm test -- --coverage

# =============================================================================
# 🐳 MODO DOCKER - CALIDAD DE CÓDIGO
# =============================================================================

lint: ## [DOCKER] Verificar código con ESLint
	@echo "$(GREEN)🔍 Verificando código...$(NC)"
	cd ../.. && $(DOCKER_COMPOSE) -f $(COMPOSE_FILE) run --rm $(SERVICE_NAME) npm run lint

lint-fix: ## [DOCKER] Auto-corregir problemas de lint
	@echo "$(GREEN)🔧 Auto-corrigiendo código...$(NC)"
	cd ../.. && $(DOCKER_COMPOSE) -f $(COMPOSE_FILE) run --rm $(SERVICE_NAME) npm run lint:fix

format: ## [DOCKER] Formatear código con Prettier
	cd ../.. && $(DOCKER_COMPOSE) -f $(COMPOSE_FILE) run --rm $(SERVICE_NAME) npm run format

type-check: ## [DOCKER] Verificar tipos TypeScript
	cd ../.. && $(DOCKER_COMPOSE) -f $(COMPOSE_FILE) run --rm $(SERVICE_NAME) npm run type-check

# =============================================================================
# 🐳 MODO DOCKER - BUILD PRODUCCIÓN
# =============================================================================

build-prod: ## [DOCKER] Build para producción
	@echo "$(GREEN)🏗️  Building para producción...$(NC)"
	cd ../.. && $(DOCKER_COMPOSE) -f $(COMPOSE_FILE) run --rm $(SERVICE_NAME) npm run build
	@echo "$(GREEN)✅ Build de producción completado en dist/$(NC)"

preview: ## [DOCKER] Preview del build de producción
	cd ../.. && $(DOCKER_COMPOSE) -f $(COMPOSE_FILE) run --rm --service-ports $(SERVICE_NAME) npm run preview

# =============================================================================
# 🐍 MODO LOCAL - SETUP
# =============================================================================

local-setup: ## [LOCAL] Instalar dependencias localmente
	@echo "$(GREEN)🔧 Instalando dependencias...$(NC)"
	@if ! command -v node >/dev/null 2>&1; then \
		echo "$(RED)❌ Node.js no está instalado$(NC)"; \
		exit 1; \
	fi
	@if ! command -v npm >/dev/null 2>&1; then \
		echo "$(RED)❌ npm no está instalado$(NC)"; \
		exit 1; \
	fi
	$(NPM) install
	@echo "$(GREEN)✅ Dependencias instaladas$(NC)"

local-clean: ## [LOCAL] Limpiar node_modules y cache
	@echo "$(YELLOW)🧹 Limpiando...$(NC)"
	rm -rf node_modules
	rm -rf dist
	rm -rf .vite
	rm -rf coverage
	$(NPM) cache clean --force

# =============================================================================
# 🐍 MODO LOCAL - DESARROLLO
# =============================================================================

local-dev: ## [LOCAL] Ejecutar servidor local con hot-reload
	@echo "$(GREEN)🚀 Iniciando React App local...$(NC)"
	@if [ ! -d "node_modules" ]; then \
		echo "$(RED)❌ node_modules no existe. Ejecuta 'make local-setup' primero$(NC)"; \
		exit 1; \
	fi
	@echo "$(YELLOW)Servidor en http://localhost:5173$(NC)"
	$(NPM) run dev

local-dev-host: ## [LOCAL] Ejecutar servidor accesible desde red
	@echo "$(GREEN)🚀 Iniciando React App (accesible desde red)...$(NC)"
	$(NPM) run dev -- --host

local-dev-port: ## [LOCAL] Ejecutar en puerto específico (uso: make local-dev-port PORT=3000)
	@echo "$(GREEN)🚀 Iniciando React App en puerto $(PORT)...$(NC)"
	$(NPM) run dev -- --port $(PORT)

# =============================================================================
# 🐍 MODO LOCAL - TESTING
# =============================================================================

local-test: ## [LOCAL] Ejecutar tests localmente
	@echo "$(GREEN)🧪 Ejecutando tests...$(NC)"
	$(NPM) test -- --run

local-test-watch: ## [LOCAL] Tests en modo watch
	$(NPM) test

local-test-coverage: ## [LOCAL] Tests con coverage
	@echo "$(GREEN)📊 Tests con coverage...$(NC)"
	$(NPM) test -- --coverage
	@echo "$(GREEN)✅ Coverage report en coverage/index.html$(NC)"

local-test-ui: ## [LOCAL] Abrir UI de tests (Vitest UI)
	$(NPM) test -- --ui

# =============================================================================
# 🐍 MODO LOCAL - CALIDAD
# =============================================================================

local-lint: ## [LOCAL] Verificar código
	@echo "$(GREEN)🔍 Verificando código...$(NC)"
	$(NPM) run lint

local-lint-fix: ## [LOCAL] Auto-corregir problemas
	@echo "$(GREEN)🔧 Auto-corrigiendo...$(NC)"
	$(NPM) run lint:fix

local-format: ## [LOCAL] Formatear código
	$(NPM) run format

local-format-check: ## [LOCAL] Verificar formato
	$(NPM) run format:check

local-type-check: ## [LOCAL] Verificar tipos TypeScript
	$(NPM) run type-check

# =============================================================================
# 🐍 MODO LOCAL - BUILD
# =============================================================================

local-build: ## [LOCAL] Build para producción
	@echo "$(GREEN)🏗️  Building para producción...$(NC)"
	$(NPM) run build
	@echo "$(GREEN)✅ Build completado en dist/$(NC)"

local-preview: ## [LOCAL] Preview del build de producción
	@echo "$(GREEN)👁️  Preview del build...$(NC)"
	$(NPM) run preview

local-analyze: ## [LOCAL] Analizar tamaño del bundle
	@echo "$(GREEN)📊 Analizando bundle...$(NC)"
	$(NPM) run build -- --mode analyze

# =============================================================================
# 🔧 UTILIDADES
# =============================================================================

deps-update: ## Ver dependencias desactualizadas
	@echo "$(GREEN)📦 Verificando actualizaciones...$(NC)"
	$(NPM) outdated

deps-install: ## Instalar nueva dependencia (uso: make deps-install PKG=nombre)
	@echo "$(GREEN)📦 Instalando $(PKG)...$(NC)"
	$(NPM) install $(PKG)

deps-install-dev: ## Instalar dependencia de desarrollo (uso: make deps-install-dev PKG=nombre)
	@echo "$(GREEN)📦 Instalando $(PKG) como dev...$(NC)"
	$(NPM) install -D $(PKG)

deps-audit: ## Auditar vulnerabilidades
	$(NPM) audit

deps-audit-fix: ## Arreglar vulnerabilidades automáticamente
	$(NPM) audit fix

health: ## Verificar health del servicio
	@curl -s http://localhost | head -n 1 || echo "$(RED)Servicio no responde$(NC)"

health-local: ## Verificar health del servicio local
	@curl -s http://localhost:5173 | head -n 1 || echo "$(RED)Servicio no responde$(NC)"

# =============================================================================
# 🎯 WORKFLOWS COMPLETOS
# =============================================================================

first-run: local-setup ## Primera ejecución (instalar deps)
	@echo "$(GREEN)✅ Setup completado$(NC)"
	@echo "$(YELLOW)Siguiente: make local-dev o make dev$(NC)"

ci: ## Simular CI/CD localmente
	@$(MAKE) local-lint
	@$(MAKE) local-type-check
	@$(MAKE) local-test
	@$(MAKE) local-build
	@echo "$(GREEN)✅ CI pipeline OK$(NC)"

clean-all: local-clean local-setup ## Reinstalación limpia
	@echo "$(GREEN)✅ Reinstalación completada$(NC)"

# =============================================================================
# FIN DEL MAKEFILE
# =============================================================================
