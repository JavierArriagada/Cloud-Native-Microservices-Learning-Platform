# =============================================================================
# Cloud-Native Microservices Learning Platform - Makefile Principal
# =============================================================================
# Descripción: Orquestación de comandos para todo el proyecto
# Requisitos: Docker, Docker Compose v2, Make
# Documentación: docs/makefiles/README.md
# =============================================================================
#
# ESTRUCTURA DE MAKEFILES:
#   - Makefile (este)              -> Comandos de orquestación del proyecto
#   - services/api/Makefile        -> Comandos específicos de FastAPI
#   - services/dash-app/Makefile   -> Comandos específicos de Dash
#   - services/react-app/Makefile  -> Comandos específicos de React
#   - infrastructure/Makefile      -> Comandos de infraestructura y monitoreo
#
# FILOSOFÍA:
#   - Este Makefile orquesta comandos de alto nivel
#   - Para desarrollo específico de un servicio, usar su Makefile
#   - Soporta desarrollo con Docker (default) y local (Python/Node local)
#
# =============================================================================

.PHONY: help
.DEFAULT_GOAL := help

# Variables
COMPOSE_FILE := infrastructure/docker/docker-compose.yml
COMPOSE_DEV := infrastructure/docker/docker-compose.dev.yml
COMPOSE_MONITORING := infrastructure/docker/docker-compose.monitoring.yml
PROJECT_NAME := mlp

# Paths a Makefiles de servicios
API_DIR := services/api
DASH_DIR := services/dash-app
REACT_DIR := services/react-app
INFRA_DIR := infrastructure

# Colores para output
RED := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[0;33m
BLUE := \033[0;34m
MAGENTA := \033[0;35m
CYAN := \033[0;36m
NC := \033[0m

# =============================================================================
# 📋 AYUDA Y UTILIDADES
# =============================================================================

help: ## Mostrar esta ayuda
	@echo "$(BLUE)═══════════════════════════════════════════════════════════════$(NC)"
	@echo "$(GREEN)  Cloud-Native Microservices Learning Platform$(NC)"
	@echo "$(BLUE)═══════════════════════════════════════════════════════════════$(NC)"
	@echo ""
	@echo "$(CYAN)📚 COMANDOS PRINCIPALES:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		grep -v "SERVICE\|INFRA" | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-25s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(CYAN)🔧 COMANDOS DE SERVICIOS INDIVIDUALES:$(NC)"
	@echo "  $(YELLOW)make api-*$(NC)              Comandos del servicio FastAPI"
	@echo "  $(YELLOW)make dash-*$(NC)             Comandos del servicio Dash"
	@echo "  $(YELLOW)make react-*$(NC)            Comandos del servicio React"
	@echo "  $(YELLOW)make infra-*$(NC)            Comandos de infraestructura"
	@echo ""
	@echo "$(CYAN)📖 DOCUMENTACIÓN:$(NC)"
	@echo "  Para ver comandos específicos de cada servicio:"
	@echo "    $(YELLOW)cd services/api && make help$(NC)"
	@echo "    $(YELLOW)cd services/dash-app && make help$(NC)"
	@echo "    $(YELLOW)cd services/react-app && make help$(NC)"
	@echo "    $(YELLOW)cd infrastructure && make help$(NC)"
	@echo ""
	@echo "  Documentación completa: $(CYAN)docs/makefiles/README.md$(NC)"
	@echo ""

check-deps: ## Verificar prerequisitos instalados
	@echo "$(BLUE)Verificando prerequisitos...$(NC)"
	@command -v docker >/dev/null 2>&1 || { echo "$(RED)❌ Docker no instalado$(NC)"; exit 1; }
	@command -v docker compose >/dev/null 2>&1 || { echo "$(RED)❌ Docker Compose v2 no instalado$(NC)"; exit 1; }
	@command -v git >/dev/null 2>&1 || { echo "$(RED)❌ Git no instalado$(NC)"; exit 1; }
	@echo "$(GREEN)✅ Todos los prerequisitos instalados$(NC)"

urls: ## Mostrar URLs de todos los servicios
	@echo "$(BLUE)═══════════════════════════════════════════════════════════════$(NC)"
	@echo "$(GREEN)  URLs de Servicios$(NC)"
	@echo "$(BLUE)═══════════════════════════════════════════════════════════════$(NC)"
	@echo ""
	@echo "  $(CYAN)Gateway & Frontend:$(NC)"
	@echo "    React App:         $(YELLOW)http://localhost$(NC)"
	@echo "    Traefik Dashboard: $(YELLOW)http://localhost:8080$(NC)"
	@echo ""
	@echo "  $(CYAN)Backend Services:$(NC)"
	@echo "    FastAPI:           $(YELLOW)http://localhost/api$(NC)"
	@echo "    FastAPI Docs:      $(YELLOW)http://localhost/api/docs$(NC)"
	@echo "    Dash Dashboard:    $(YELLOW)http://localhost/dash$(NC)"
	@echo ""
	@echo "  $(CYAN)Monitoring:$(NC)"
	@echo "    Prometheus:        $(YELLOW)http://localhost/prometheus$(NC) (or :9090)"
	@echo "    Grafana:           $(YELLOW)http://localhost/grafana$(NC) (or :3001) - admin/admin"
	@echo "    Loki:              $(YELLOW)http://localhost/loki$(NC) (or :3100)"
	@echo ""
	@echo "  $(CYAN)Database:$(NC)"
	@echo "    PostgreSQL:        $(YELLOW)localhost:5432$(NC)"
	@echo ""

# =============================================================================
# 🚀 DESARROLLO - ORQUESTACIÓN COMPLETA
# =============================================================================

dev-up: ## Levantar todos los servicios en desarrollo
	@echo "$(GREEN)🚀 Levantando servicios...$(NC)"
	@if [ ! -f .env ]; then \
		echo "$(YELLOW)⚠️  .env no existe, copiando desde .env.example...$(NC)"; \
		cp .env.example .env; \
	fi
	docker compose -f $(COMPOSE_FILE) -f $(COMPOSE_DEV) up -d
	@echo "$(GREEN)✅ Servicios levantados$(NC)"
	@$(MAKE) urls

dev-down: ## Detener todos los servicios
	@echo "$(YELLOW)⏹️  Deteniendo servicios...$(NC)"
	docker compose -f $(COMPOSE_FILE) -f $(COMPOSE_DEV) down
	@echo "$(GREEN)✅ Servicios detenidos$(NC)"

dev-restart: ## Reiniciar todos los servicios
	@$(MAKE) dev-down
	@$(MAKE) dev-up

dev-logs: ## Ver logs de todos los servicios
	docker compose -f $(COMPOSE_FILE) -f $(COMPOSE_DEV) logs -f

dev-status: ## Ver estado de containers
	@echo "$(CYAN)Estado de servicios:$(NC)"
	docker compose -f $(COMPOSE_FILE) -f $(COMPOSE_DEV) ps

dev-full: ## Levantar servicios + monitoreo
	@$(MAKE) dev-up
	@$(MAKE) monitoring-up
	@echo "$(GREEN)✅ Stack completo activo$(NC)"

# =============================================================================
# 🐳 SERVICIOS INDIVIDUALES - API (FastAPI)
# =============================================================================

api-dev: ## [SERVICE] Levantar solo API en Docker
	@$(MAKE) -C $(API_DIR) dev

api-stop: ## [SERVICE] Detener API
	@$(MAKE) -C $(API_DIR) stop

api-logs: ## [SERVICE] Ver logs de API
	@$(MAKE) -C $(API_DIR) logs

api-shell: ## [SERVICE] Shell en container API
	@$(MAKE) -C $(API_DIR) shell

api-test: ## [SERVICE] Tests de API
	@$(MAKE) -C $(API_DIR) test

api-local: ## [SERVICE] Ejecutar API en modo local (Python)
	@echo "$(CYAN)💡 Ejecutando API en modo local...$(NC)"
	@$(MAKE) -C $(API_DIR) local-dev

api-setup: ## [SERVICE] Setup entorno local de API
	@$(MAKE) -C $(API_DIR) local-setup

# =============================================================================
# 🐳 SERVICIOS INDIVIDUALES - DASH
# =============================================================================

dash-dev: ## [SERVICE] Levantar solo Dash en Docker
	@$(MAKE) -C $(DASH_DIR) dev

dash-stop: ## [SERVICE] Detener Dash
	@$(MAKE) -C $(DASH_DIR) stop

dash-logs: ## [SERVICE] Ver logs de Dash
	@$(MAKE) -C $(DASH_DIR) logs

dash-shell: ## [SERVICE] Shell en container Dash
	@$(MAKE) -C $(DASH_DIR) shell

dash-local: ## [SERVICE] Ejecutar Dash en modo local (Python)
	@echo "$(CYAN)💡 Ejecutando Dash en modo local...$(NC)"
	@$(MAKE) -C $(DASH_DIR) local-dev

dash-setup: ## [SERVICE] Setup entorno local de Dash
	@$(MAKE) -C $(DASH_DIR) local-setup

# =============================================================================
# 🐳 SERVICIOS INDIVIDUALES - REACT
# =============================================================================

react-dev: ## [SERVICE] Levantar solo React en Docker
	@$(MAKE) -C $(REACT_DIR) dev

react-stop: ## [SERVICE] Detener React
	@$(MAKE) -C $(REACT_DIR) stop

react-logs: ## [SERVICE] Ver logs de React
	@$(MAKE) -C $(REACT_DIR) logs

react-shell: ## [SERVICE] Shell en container React
	@$(MAKE) -C $(REACT_DIR) shell

react-test: ## [SERVICE] Tests de React
	@$(MAKE) -C $(REACT_DIR) test

react-local: ## [SERVICE] Ejecutar React en modo local (Node.js)
	@echo "$(CYAN)💡 Ejecutando React en modo local...$(NC)"
	@$(MAKE) -C $(REACT_DIR) local-dev

react-setup: ## [SERVICE] Setup entorno local de React
	@$(MAKE) -C $(REACT_DIR) local-setup

# =============================================================================
# 📊 INFRAESTRUCTURA Y MONITOREO
# =============================================================================

monitoring-up: ## [INFRA] Levantar stack de monitoreo
	@$(MAKE) -C $(INFRA_DIR) monitoring-up

monitoring-down: ## [INFRA] Detener monitoreo
	@$(MAKE) -C $(INFRA_DIR) monitoring-down

monitoring-logs: ## [INFRA] Ver logs de monitoreo
	@$(MAKE) -C $(INFRA_DIR) monitoring-logs

infra-health: ## [INFRA] Health check de todos los servicios
	@$(MAKE) -C $(INFRA_DIR) health-all

infra-stats: ## [INFRA] Ver estadísticas de containers
	@$(MAKE) -C $(INFRA_DIR) docker-stats

infra-network: ## [INFRA] Diagnosticar redes
	@$(MAKE) -C $(INFRA_DIR) network-ls

# =============================================================================
# 🔨 BUILD
# =============================================================================

build: ## Build todas las imágenes
	@echo "$(GREEN)🔨 Building todas las imágenes...$(NC)"
	docker compose -f $(COMPOSE_FILE) build --no-cache
	@echo "$(GREEN)✅ Build completado$(NC)"

build-api: ## Build solo API
	@echo "$(GREEN)🔨 Building API...$(NC)"
	docker compose -f $(COMPOSE_FILE) build --no-cache api

build-dash: ## Build solo Dash
	@echo "$(GREEN)🔨 Building Dash...$(NC)"
	docker compose -f $(COMPOSE_FILE) build --no-cache dash

build-react: ## Build solo React
	@echo "$(GREEN)🔨 Building React...$(NC)"
	docker compose -f $(COMPOSE_FILE) build --no-cache react

rebuild: dev-down build dev-up ## Rebuild completo y restart

# =============================================================================
# 🧪 TESTING Y CALIDAD
# =============================================================================

test: ## Ejecutar todos los tests
	@echo "$(GREEN)🧪 Ejecutando tests...$(NC)"
	@$(MAKE) -C $(API_DIR) test
	@$(MAKE) -C $(REACT_DIR) test
	@echo "$(GREEN)✅ Todos los tests pasaron$(NC)"

test-coverage: ## Tests con coverage
	@$(MAKE) -C $(API_DIR) test-cov
	@$(MAKE) -C $(REACT_DIR) test-coverage

lint: ## Verificar código (lint)
	@echo "$(GREEN)🔍 Verificando código...$(NC)"
	@$(MAKE) -C $(API_DIR) lint
	@$(MAKE) -C $(DASH_DIR) lint
	@$(MAKE) -C $(REACT_DIR) lint
	@echo "$(GREEN)✅ Lint completado$(NC)"

lint-fix: ## Auto-corregir problemas de lint
	@echo "$(GREEN)🔧 Auto-corrigiendo...$(NC)"
	@$(MAKE) -C $(API_DIR) lint-fix
	@$(MAKE) -C $(DASH_DIR) lint-fix
	@$(MAKE) -C $(REACT_DIR) lint-fix

format: ## Formatear código
	@echo "$(GREEN)✨ Formateando código...$(NC)"
	@$(MAKE) -C $(API_DIR) format
	@$(MAKE) -C $(DASH_DIR) format
	@$(MAKE) -C $(REACT_DIR) format

# =============================================================================
# 🐘 DATABASE
# =============================================================================

db-shell: ## Conectar a PostgreSQL via psql
	docker compose -f $(COMPOSE_FILE) exec postgres psql -U mlp_user -d mlp_db

db-migrate: ## Ejecutar migraciones
	@$(MAKE) -C $(API_DIR) db-migrate

db-migrate-create: ## Crear nueva migración (uso: make db-migrate-create MSG="mensaje")
	@$(MAKE) -C $(API_DIR) db-migrate-create MSG="$(MSG)"

db-migrate-down: ## Revertir última migración
	@$(MAKE) -C $(API_DIR) db-migrate-down

db-seed: ## Cargar datos de ejemplo
	@$(MAKE) -C $(API_DIR) db-seed

db-reset: ## Reset completo de base de datos (¡PELIGRO!)
	@echo "$(RED)⚠️  ADVERTENCIA: Esto eliminará todos los datos$(NC)"
	@read -p "¿Estás seguro? [y/N]: " confirm && [ "$$confirm" = "y" ] || exit 1
	docker compose -f $(COMPOSE_FILE) down -v
	docker compose -f $(COMPOSE_FILE) up -d postgres
	@sleep 5
	@$(MAKE) db-migrate

db-backup: ## Backup de base de datos
	@echo "$(GREEN)💾 Creando backup...$(NC)"
	docker compose -f $(COMPOSE_FILE) exec postgres pg_dump -U mlp_user mlp_db > backup_$(shell date +%Y%m%d_%H%M%S).sql
	@echo "$(GREEN)✅ Backup creado$(NC)"

# =============================================================================
# ☁️ CLOUD / KUBERNETES
# =============================================================================

k8s-context: ## Ver contexto actual de Kubernetes
	@$(MAKE) -C $(INFRA_DIR) k8s-context

k8s-apply-dev: ## Aplicar manifests a cluster dev
	@$(MAKE) -C $(INFRA_DIR) k8s-apply-dev

k8s-apply-prod: ## Aplicar manifests a producción
	@$(MAKE) -C $(INFRA_DIR) k8s-apply-prod

k8s-status: ## Ver estado de pods
	@$(MAKE) -C $(INFRA_DIR) k8s-pods

deploy-staging: ## Deploy a staging
	@echo "$(GREEN)🚀 Deploying a staging...$(NC)"
	@$(MAKE) k8s-apply-dev
	@echo "$(GREEN)✅ Deploy a staging completado$(NC)"

deploy-prod: ## Deploy a producción
	@echo "$(RED)⚠️  Deploy a PRODUCCIÓN$(NC)"
	@read -p "¿Confirmas deploy a PRODUCCIÓN? [y/N]: " confirm && [ "$$confirm" = "y" ] || exit 1
	@$(MAKE) k8s-apply-prod
	@echo "$(GREEN)✅ Deploy a producción completado$(NC)"

# =============================================================================
# 🧹 LIMPIEZA
# =============================================================================

clean: ## Limpiar containers y volumes
	@echo "$(YELLOW)🧹 Limpiando...$(NC)"
	docker compose -f $(COMPOSE_FILE) -f $(COMPOSE_DEV) down -v
	docker compose -f $(COMPOSE_MONITORING) down -v
	@echo "$(GREEN)✅ Limpieza completada$(NC)"

clean-services: ## Limpiar entornos locales de servicios
	@echo "$(YELLOW)Limpiando entornos locales...$(NC)"
	@$(MAKE) -C $(API_DIR) local-clean
	@$(MAKE) -C $(DASH_DIR) local-clean
	@$(MAKE) -C $(REACT_DIR) local-clean

clean-images: ## Eliminar imágenes del proyecto
	@$(MAKE) -C $(INFRA_DIR) docker-images-rm

clean-all: ## Limpieza profunda (containers, volumes, images, entornos locales)
	@echo "$(RED)⚠️  Limpieza profunda$(NC)"
	@$(MAKE) clean
	@$(MAKE) clean-services
	@$(MAKE) clean-images
	docker system prune -f

# =============================================================================
# 🔄 CI/CD LOCAL
# =============================================================================

ci-local: ## Simular pipeline CI localmente
	@echo "$(GREEN)🔄 Ejecutando CI local...$(NC)"
	@$(MAKE) lint
	@$(MAKE) test
	@$(MAKE) build
	@echo "$(GREEN)✅ CI local completado$(NC)"

pre-commit: ## Ejecutar checks pre-commit
	@$(MAKE) lint
	@$(MAKE) -C $(API_DIR) test

# =============================================================================
# 📦 DOCKER REGISTRY
# =============================================================================

docker-login: ## Login a Docker registry
	docker login

docker-push: ## Push imágenes a registry
	@echo "$(GREEN)📤 Pushing imágenes...$(NC)"
	docker compose -f $(COMPOSE_FILE) push

docker-pull: ## Pull imágenes desde registry
	@echo "$(GREEN)📥 Pulling imágenes...$(NC)"
	docker compose -f $(COMPOSE_FILE) pull

# =============================================================================
# 🔍 DEBUGGING
# =============================================================================

debug-network: ## Ver redes Docker
	@$(MAKE) -C $(INFRA_DIR) network-ls

debug-volumes: ## Ver volumes Docker
	@$(MAKE) -C $(INFRA_DIR) docker-volumes-ls

debug-env: ## Mostrar variables de entorno
	@echo "$(BLUE)Variables de entorno desde .env:$(NC)"
	@cat .env 2>/dev/null || echo "$(RED).env no existe$(NC)"

health-check: ## Verificar health de todos los servicios
	@$(MAKE) -C $(INFRA_DIR) health-all

# =============================================================================
# 📝 DOCUMENTACIÓN
# =============================================================================

docs-serve: ## Servir documentación local
	@echo "$(GREEN)📖 Sirviendo documentación en http://localhost:8888...$(NC)"
	@command -v python3 >/dev/null 2>&1 && cd docs && python3 -m http.server 8888 || echo "$(RED)Python no instalado$(NC)"

docs-api: ## Abrir API docs en browser
	@echo "$(GREEN)Abriendo API docs...$(NC)"
	xdg-open http://localhost/api/docs 2>/dev/null || open http://localhost/api/docs 2>/dev/null || echo "Abrir manualmente: http://localhost/api/docs"

docs-makefiles: ## Abrir documentación de Makefiles
	@echo "$(CYAN)Documentación de Makefiles: docs/makefiles/README.md$(NC)"

# =============================================================================
# 🎯 WORKFLOWS COMPLETOS
# =============================================================================

first-run: check-deps ## Primera ejecución del proyecto
	@echo "$(BLUE)═══════════════════════════════════════════════════════════════$(NC)"
	@echo "$(GREEN)  Primera ejecución - Cloud Native Microservices$(NC)"
	@echo "$(BLUE)═══════════════════════════════════════════════════════════════$(NC)"
	@echo ""
	@if [ ! -f .env ]; then \
		echo "$(YELLOW)Creando .env desde .env.example...$(NC)"; \
		cp .env.example .env; \
	fi
	@echo "$(GREEN)✅ Configuración inicial completa$(NC)"
	@echo ""
	@echo "$(YELLOW)Siguiente paso: make dev-up$(NC)"
	@echo "$(YELLOW)O para modo local: make api-setup && make react-setup$(NC)"

setup-local-all: ## Setup entornos locales de todos los servicios
	@echo "$(GREEN)🔧 Configurando entornos locales...$(NC)"
	@$(MAKE) -C $(API_DIR) local-setup
	@$(MAKE) -C $(DASH_DIR) local-setup
	@$(MAKE) -C $(REACT_DIR) local-setup
	@echo "$(GREEN)✅ Todos los entornos locales configurados$(NC)"

reset-project: ## Reset completo del proyecto
	@echo "$(RED)⚠️  ADVERTENCIA: Reset completo del proyecto$(NC)"
	@read -p "Esto eliminará TODOS los datos y containers. ¿Continuar? [y/N]: " confirm && [ "$$confirm" = "y" ] || exit 1
	@$(MAKE) clean-all
	@$(MAKE) first-run
	@echo "$(GREEN)✅ Proyecto reseteado$(NC)"

# =============================================================================
# 📊 STATUS Y MONITORING
# =============================================================================

status: ## Ver estado completo del proyecto
	@echo "$(BLUE)═══════════════════════════════════════════════════════════════$(NC)"
	@echo "$(GREEN)  Estado del Proyecto$(NC)"
	@echo "$(BLUE)═══════════════════════════════════════════════════════════════$(NC)"
	@echo ""
	@$(MAKE) dev-status
	@echo ""
	@$(MAKE) health-check
	@echo ""

# =============================================================================
# FIN DEL MAKEFILE
# =============================================================================
