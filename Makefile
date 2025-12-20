# =============================================================================
# Cloud-Native Microservices Learning Platform - Makefile
# =============================================================================
# Descripción: Comandos centralizados para desarrollo, testing, deploy y ops
# Requisitos: Docker, Docker Compose v2, Make
# =============================================================================

.PHONY: help
.DEFAULT_GOAL := help

# Variables
COMPOSE_FILE := infrastructure/docker/docker-compose.yml
COMPOSE_DEV := infrastructure/docker/docker-compose.dev.yml
COMPOSE_MONITORING := infrastructure/docker/docker-compose.monitoring.yml
PROJECT_NAME := mlp

# Colores para output
RED := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[0;33m
BLUE := \033[0;34m
NC := \033[0m # No Color

# =============================================================================
# 📋 AYUDA Y UTILIDADES
# =============================================================================

help: ## Mostrar esta ayuda
	@echo "$(BLUE)═══════════════════════════════════════════════════════════════$(NC)"
	@echo "$(GREEN)  Cloud-Native Microservices Learning Platform$(NC)"
	@echo "$(BLUE)═══════════════════════════════════════════════════════════════$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, $$2}'
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
	@echo "  $(YELLOW)Gateway & Frontend:$(NC)"
	@echo "    React App:         http://localhost"
	@echo "    Traefik Dashboard: http://localhost:8080"
	@echo ""
	@echo "  $(YELLOW)Backend Services:$(NC)"
	@echo "    FastAPI:           http://localhost/api"
	@echo "    FastAPI Docs:      http://localhost/api/docs"
	@echo "    Dash Dashboard:    http://localhost/dash"
	@echo ""
	@echo "  $(YELLOW)Monitoring:$(NC)"
	@echo "    Prometheus:        http://localhost/prometheus"
	@echo "    Grafana:           http://localhost/grafana (admin/admin)"
	@echo "    Loki:              http://localhost/loki"
	@echo ""
	@echo "  $(YELLOW)Monitoring (Direct Access):$(NC)"
	@echo "    Prometheus:        http://localhost:9090"
	@echo "    Grafana:           http://localhost:3001"
	@echo "    Loki:              http://localhost:3100"
	@echo ""
	@echo "  $(YELLOW)Database:$(NC)"
	@echo "    PostgreSQL:        localhost:5432"
	@echo ""

# =============================================================================
# 🚀 DESARROLLO LOCAL
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

dev-logs-api: ## Ver logs solo de API
	docker compose -f $(COMPOSE_FILE) -f $(COMPOSE_DEV) logs -f api

dev-logs-dash: ## Ver logs solo de Dash
	docker compose -f $(COMPOSE_FILE) -f $(COMPOSE_DEV) logs -f dash

dev-logs-react: ## Ver logs solo de React
	docker compose -f $(COMPOSE_FILE) -f $(COMPOSE_DEV) logs -f react

dev-status: ## Ver estado de containers
	docker compose -f $(COMPOSE_FILE) -f $(COMPOSE_DEV) ps

dev-shell-api: ## Abrir shell en container API
	docker compose -f $(COMPOSE_FILE) -f $(COMPOSE_DEV) exec api /bin/sh

dev-shell-dash: ## Abrir shell en container Dash
	docker compose -f $(COMPOSE_FILE) -f $(COMPOSE_DEV) exec dash /bin/sh

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
	@$(MAKE) test-api
	@$(MAKE) test-react
	@echo "$(GREEN)✅ Todos los tests pasaron$(NC)"

test-api: ## Tests de API
	@echo "$(YELLOW)Testing API...$(NC)"
	docker compose -f $(COMPOSE_FILE) run --rm api pytest tests/ -v

test-react: ## Tests de React
	@echo "$(YELLOW)Testing React...$(NC)"
	docker compose -f $(COMPOSE_FILE) run --rm react npm test

test-integration: ## Tests de integración
	@echo "$(YELLOW)Tests de integración...$(NC)"
	docker compose -f $(COMPOSE_FILE) run --rm api pytest tests/integration/ -v

test-coverage: ## Tests con coverage
	docker compose -f $(COMPOSE_FILE) run --rm api pytest --cov=app --cov-report=html tests/

lint: ## Verificar código (lint)
	@echo "$(GREEN)🔍 Verificando código...$(NC)"
	@$(MAKE) lint-api
	@$(MAKE) lint-react
	@echo "$(GREEN)✅ Lint completado$(NC)"

lint-api: ## Lint API Python
	@echo "$(YELLOW)Linting API...$(NC)"
	docker compose -f $(COMPOSE_FILE) run --rm api ruff check .
	docker compose -f $(COMPOSE_FILE) run --rm api black --check .

lint-react: ## Lint React TypeScript
	@echo "$(YELLOW)Linting React...$(NC)"
	docker compose -f $(COMPOSE_FILE) run --rm react npm run lint

lint-fix: ## Auto-corregir problemas de lint
	@echo "$(GREEN)🔧 Auto-corrigiendo...$(NC)"
	docker compose -f $(COMPOSE_FILE) run --rm api ruff check --fix .
	docker compose -f $(COMPOSE_FILE) run --rm api black .
	docker compose -f $(COMPOSE_FILE) run --rm react npm run lint:fix

format: ## Formatear código
	@echo "$(GREEN)✨ Formateando código...$(NC)"
	docker compose -f $(COMPOSE_FILE) run --rm api black .
	docker compose -f $(COMPOSE_FILE) run --rm react npm run format

# =============================================================================
# 🐘 DATABASE
# =============================================================================

db-shell: ## Conectar a PostgreSQL via psql
	docker compose -f $(COMPOSE_FILE) exec postgres psql -U mlp_user -d mlp_db

db-migrate: ## Ejecutar migraciones
	@echo "$(GREEN)📦 Ejecutando migraciones...$(NC)"
	docker compose -f $(COMPOSE_FILE) exec api alembic upgrade head

db-migrate-create: ## Crear nueva migración (uso: make db-migrate-create MSG="mensaje")
	@echo "$(GREEN)📝 Creando migración...$(NC)"
	docker compose -f $(COMPOSE_FILE) exec api alembic revision --autogenerate -m "$(MSG)"

db-migrate-down: ## Revertir última migración
	docker compose -f $(COMPOSE_FILE) exec api alembic downgrade -1

db-migrate-history: ## Ver historial de migraciones
	docker compose -f $(COMPOSE_FILE) exec api alembic history

db-seed: ## Cargar datos de ejemplo
	@echo "$(GREEN)🌱 Cargando datos de ejemplo...$(NC)"
	docker compose -f $(COMPOSE_FILE) exec api python -m scripts.seed_data

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
# 📊 MONITOREO
# =============================================================================

monitoring-up: ## Levantar stack de monitoreo
	@echo "$(GREEN)📊 Levantando monitoreo...$(NC)"
	docker compose -f $(COMPOSE_MONITORING) up -d
	@echo "$(GREEN)✅ Monitoreo activo$(NC)"
	@echo "  Prometheus: http://localhost/prometheus (or :9090)"
	@echo "  Grafana:    http://localhost/grafana (or :3001)"
	@echo "  Loki:       http://localhost/loki (or :3100)"

monitoring-down: ## Detener monitoreo
	docker compose -f $(COMPOSE_MONITORING) down

monitoring-logs: ## Ver logs de monitoreo
	docker compose -f $(COMPOSE_MONITORING) logs -f

monitoring-restart: ## Reiniciar monitoreo
	@$(MAKE) monitoring-down
	@$(MAKE) monitoring-up

# =============================================================================
# ☁️ CLOUD / KUBERNETES
# =============================================================================

k8s-context: ## Ver contexto actual de Kubernetes
	kubectl config current-context

k8s-apply-dev: ## Aplicar manifests a cluster dev
	kubectl apply -k infrastructure/kubernetes/overlays/staging

k8s-apply-prod: ## Aplicar manifests a producción
	kubectl apply -k infrastructure/kubernetes/overlays/production

k8s-delete-dev: ## Eliminar recursos de dev
	kubectl delete -k infrastructure/kubernetes/overlays/staging

k8s-status: ## Ver estado de pods
	kubectl get pods -n mlp

k8s-logs: ## Ver logs de pod (uso: make k8s-logs POD=nombre-pod)
	kubectl logs -f $(POD) -n mlp

k8s-shell: ## Shell en pod (uso: make k8s-shell POD=nombre-pod)
	kubectl exec -it $(POD) -n mlp -- /bin/sh

k8s-port-forward: ## Port forward API (8000:8000)
	kubectl port-forward -n mlp service/api 8000:8000

deploy-staging: ## Deploy a staging (GCP)
	@echo "$(GREEN)🚀 Deploying a staging...$(NC)"
	@$(MAKE) k8s-apply-dev
	@echo "$(GREEN)✅ Deploy a staging completado$(NC)"

deploy-prod: ## Deploy a producción (GCP)
	@echo "$(RED)⚠️  Deploy a PRODUCCIÓN$(NC)"
	@read -p "¿Confirmas deploy a PRODUCCIÓN? [y/N]: " confirm && [ "$$confirm" = "y" ] || exit 1
	@$(MAKE) k8s-apply-prod
	@echo "$(GREEN)✅ Deploy a producción completado$(NC)"

# =============================================================================
# 🧹 LIMPIEZA
# =============================================================================

clean: ## Limpiar containers, volumes y build artifacts
	@echo "$(YELLOW)🧹 Limpiando...$(NC)"
	docker compose -f $(COMPOSE_FILE) -f $(COMPOSE_DEV) down -v
	docker compose -f $(COMPOSE_MONITORING) down -v
	@echo "$(GREEN)✅ Limpieza completada$(NC)"

clean-volumes: ## Eliminar solo volumes
	docker compose -f $(COMPOSE_FILE) down -v

clean-images: ## Eliminar imágenes del proyecto
	docker rmi $(shell docker images -q '$(PROJECT_NAME)/*') 2>/dev/null || true

clean-all: ## Limpieza profunda (containers, volumes, images)
	@echo "$(RED)⚠️  Limpieza profunda$(NC)"
	@$(MAKE) clean
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
	@$(MAKE) test-api

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
	docker network ls
	docker network inspect $(PROJECT_NAME)_frontend || true
	docker network inspect $(PROJECT_NAME)_backend || true

debug-volumes: ## Ver volumes Docker
	docker volume ls | grep $(PROJECT_NAME)

debug-api: ## Debug API (adjunta debugger)
	docker compose -f $(COMPOSE_FILE) -f $(COMPOSE_DEV) run --rm --service-ports api

debug-env: ## Mostrar variables de entorno
	@echo "$(BLUE)Variables de entorno desde .env:$(NC)"
	@cat .env 2>/dev/null || echo "$(RED).env no existe$(NC)"

health-check: ## Verificar health de todos los servicios
	@echo "$(GREEN)🏥 Verificando salud de servicios...$(NC)"
	@curl -s http://localhost/api/health | jq . || echo "$(RED)API no responde$(NC)"
	@curl -s http://localhost:9090/-/healthy || echo "$(RED)Prometheus no responde$(NC)"
	@curl -s http://localhost:3001/api/health || echo "$(RED)Grafana no responde$(NC)"

# =============================================================================
# 📝 DOCUMENTACIÓN
# =============================================================================

docs-serve: ## Servir documentación local
	@echo "$(GREEN)📖 Sirviendo documentación...$(NC)"
	@command -v python3 >/dev/null 2>&1 && cd docs && python3 -m http.server 8888 || echo "$(RED)Python no instalado$(NC)"

docs-api: ## Abrir API docs en browser
	@echo "$(GREEN)Abriendo API docs...$(NC)"
	xdg-open http://localhost/api/docs 2>/dev/null || open http://localhost/api/docs 2>/dev/null || echo "Abrir manualmente: http://localhost/api/docs"

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

reset-project: ## Reset completo del proyecto
	@echo "$(RED)⚠️  ADVERTENCIA: Reset completo del proyecto$(NC)"
	@read -p "Esto eliminará TODOS los datos y containers. ¿Continuar? [y/N]: " confirm && [ "$$confirm" = "y" ] || exit 1
	@$(MAKE) clean-all
	@$(MAKE) first-run
	@echo "$(GREEN)✅ Proyecto reseteado$(NC)"

# =============================================================================
# FIN DEL MAKEFILE
# =============================================================================
