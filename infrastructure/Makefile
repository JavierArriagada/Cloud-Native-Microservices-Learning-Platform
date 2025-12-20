# =============================================================================
# Infrastructure - Makefile
# =============================================================================
# Descripción: Comandos para gestión de infraestructura, monitoreo y operaciones
# Incluye: Docker, Kubernetes, Monitoreo, Networking, Debugging
# =============================================================================

.PHONY: help
.DEFAULT_GOAL := help

# Variables
DOCKER_COMPOSE := docker compose
COMPOSE_FILE := docker/docker-compose.yml
COMPOSE_DEV := docker/docker-compose.dev.yml
COMPOSE_MONITORING := docker/docker-compose.monitoring.yml
PROJECT_NAME := mlp

# Colores
RED := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[0;33m
BLUE := \033[0;34m
MAGENTA := \033[0;35m
CYAN := \033[0;36m
NC := \033[0m

# =============================================================================
# 📋 AYUDA
# =============================================================================

help: ## Mostrar esta ayuda
	@echo "$(BLUE)═══════════════════════════════════════════════════════════$(NC)"
	@echo "$(GREEN)  Infrastructure Management - Comandos$(NC)"
	@echo "$(BLUE)═══════════════════════════════════════════════════════════$(NC)"
	@echo ""
	@echo "$(CYAN)📊 MONITOREO:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		grep "MONITOR" | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-30s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(CYAN)🐳 DOCKER:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		grep "DOCKER" | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-30s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(CYAN)🌐 NETWORKING:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		grep "NETWORK" | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-30s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(CYAN)☸️  KUBERNETES:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		grep "K8S" | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-30s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(CYAN)🔍 DEBUGGING:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		grep "DEBUG" | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-30s$(NC) %s\n", $$1, $$2}'
	@echo ""

# =============================================================================
# 📊 MONITOREO - GESTIÓN
# =============================================================================

monitoring-up: ## [MONITOR] Levantar stack completo de monitoreo
	@echo "$(GREEN)📊 Levantando stack de monitoreo...$(NC)"
	$(DOCKER_COMPOSE) -f $(COMPOSE_MONITORING) up -d
	@sleep 3
	@echo "$(GREEN)✅ Stack de monitoreo activo$(NC)"
	@$(MAKE) monitoring-urls

monitoring-down: ## [MONITOR] Detener stack de monitoreo
	@echo "$(YELLOW)⏹️  Deteniendo monitoreo...$(NC)"
	$(DOCKER_COMPOSE) -f $(COMPOSE_MONITORING) down

monitoring-restart: ## [MONITOR] Reiniciar stack de monitoreo
	@$(MAKE) monitoring-down
	@$(MAKE) monitoring-up

monitoring-logs: ## [MONITOR] Ver logs de todos los servicios de monitoreo
	$(DOCKER_COMPOSE) -f $(COMPOSE_MONITORING) logs -f

monitoring-status: ## [MONITOR] Ver estado de servicios de monitoreo
	@echo "$(BLUE)Estado de servicios de monitoreo:$(NC)"
	@$(DOCKER_COMPOSE) -f $(COMPOSE_MONITORING) ps

monitoring-urls: ## [MONITOR] Mostrar URLs de acceso
	@echo ""
	@echo "$(BLUE)═══════════════════════════════════════════════════════════$(NC)"
	@echo "$(GREEN)  URLs de Monitoreo$(NC)"
	@echo "$(BLUE)═══════════════════════════════════════════════════════════$(NC)"
	@echo ""
	@echo "  $(CYAN)Prometheus:$(NC)"
	@echo "    Via Traefik:  $(YELLOW)http://localhost/prometheus$(NC)"
	@echo "    Directo:      $(YELLOW)http://localhost:9090$(NC)"
	@echo ""
	@echo "  $(CYAN)Grafana:$(NC)"
	@echo "    Via Traefik:  $(YELLOW)http://localhost/grafana$(NC)"
	@echo "    Directo:      $(YELLOW)http://localhost:3001$(NC)"
	@echo "    Credenciales: $(MAGENTA)admin / admin$(NC)"
	@echo ""
	@echo "  $(CYAN)Loki:$(NC)"
	@echo "    Via Traefik:  $(YELLOW)http://localhost/loki$(NC)"
	@echo "    Directo:      $(YELLOW)http://localhost:3100$(NC)"
	@echo ""

# =============================================================================
# 📊 MONITOREO - SERVICIOS INDIVIDUALES
# =============================================================================

prometheus-up: ## [MONITOR] Levantar solo Prometheus
	@echo "$(GREEN)Starting Prometheus...$(NC)"
	$(DOCKER_COMPOSE) -f $(COMPOSE_MONITORING) up -d prometheus
	@echo "$(GREEN)✅ Prometheus: http://localhost:9090$(NC)"

prometheus-reload: ## [MONITOR] Recargar configuración de Prometheus
	@echo "$(YELLOW)Recargando configuración de Prometheus...$(NC)"
	curl -X POST http://localhost:9090/-/reload
	@echo "$(GREEN)✅ Configuración recargada$(NC)"

prometheus-targets: ## [MONITOR] Ver targets de Prometheus
	@curl -s http://localhost:9090/api/v1/targets | jq '.data.activeTargets[] | {job: .labels.job, instance: .labels.instance, health: .health}'

grafana-up: ## [MONITOR] Levantar solo Grafana
	@echo "$(GREEN)Starting Grafana...$(NC)"
	$(DOCKER_COMPOSE) -f $(COMPOSE_MONITORING) up -d grafana
	@echo "$(GREEN)✅ Grafana: http://localhost:3001$(NC)"

grafana-reset-password: ## [MONITOR] Resetear password de Grafana admin
	$(DOCKER_COMPOSE) -f $(COMPOSE_MONITORING) exec grafana grafana-cli admin reset-admin-password admin
	@echo "$(GREEN)✅ Password reseteado a 'admin'$(NC)"

loki-up: ## [MONITOR] Levantar solo Loki
	@echo "$(GREEN)Starting Loki...$(NC)"
	$(DOCKER_COMPOSE) -f $(COMPOSE_MONITORING) up -d loki
	@echo "$(GREEN)✅ Loki: http://localhost:3100$(NC)"

loki-labels: ## [MONITOR] Ver labels disponibles en Loki
	@curl -s http://localhost:3100/loki/api/v1/labels | jq .

# =============================================================================
# 📊 MONITOREO - MÉTRICAS Y QUERIES
# =============================================================================

metrics-api: ## [MONITOR] Ver métricas del servicio API
	@echo "$(CYAN)Métricas del servicio API:$(NC)"
	@curl -s http://localhost/api/metrics || echo "$(RED)API no responde$(NC)"

metrics-all: ## [MONITOR] Ver todas las métricas disponibles
	@echo "$(CYAN)Métricas de todos los servicios:$(NC)"
	@echo ""
	@echo "$(YELLOW)API:$(NC)"
	@curl -s http://localhost/api/metrics | head -20
	@echo ""

query-prom: ## [MONITOR] Query a Prometheus (uso: make query-prom Q="up")
	@curl -s "http://localhost:9090/api/v1/query?query=$(Q)" | jq .

query-loki: ## [MONITOR] Query a Loki logs (uso: make query-loki Q="{job=\"api\"}")
	@curl -s "http://localhost:3100/loki/api/v1/query?query=$(Q)" | jq .

# =============================================================================
# 🐳 DOCKER - GESTIÓN DE CONTENEDORES
# =============================================================================

docker-ps: ## [DOCKER] Listar todos los containers del proyecto
	@echo "$(CYAN)Containers del proyecto:$(NC)"
	docker ps -a --filter "name=$(PROJECT_NAME)" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

docker-stats: ## [DOCKER] Ver estadísticas de recursos en tiempo real
	docker stats --filter "name=$(PROJECT_NAME)"

docker-top: ## [DOCKER] Ver procesos corriendo en containers
	@for container in $$(docker ps --filter "name=$(PROJECT_NAME)" --format "{{.Names}}"); do \
		echo "$(CYAN)$$container:$(NC)"; \
		docker top $$container; \
		echo ""; \
	done

docker-inspect: ## [DOCKER] Inspeccionar container (uso: make docker-inspect CONTAINER=api)
	docker inspect $(PROJECT_NAME)-$(CONTAINER)-1 | jq .

docker-logs-all: ## [DOCKER] Ver logs de todos los containers
	docker logs -f --tail=100 $$(docker ps --filter "name=$(PROJECT_NAME)" --format "{{.Names}}" | head -1)

# =============================================================================
# 🐳 DOCKER - LIMPIEZA Y MANTENIMIENTO
# =============================================================================

docker-prune: ## [DOCKER] Limpiar recursos no usados
	@echo "$(YELLOW)Limpiando recursos Docker...$(NC)"
	docker system prune -f
	@echo "$(GREEN)✅ Limpieza completada$(NC)"

docker-prune-all: ## [DOCKER] Limpieza profunda (incluye volúmenes)
	@echo "$(RED)⚠️  Limpieza profunda (incluye volúmenes)$(NC)"
	@read -p "¿Continuar? [y/N]: " confirm && [ "$$confirm" = "y" ] || exit 1
	docker system prune -af --volumes

docker-images-ls: ## [DOCKER] Listar imágenes del proyecto
	docker images | grep $(PROJECT_NAME)

docker-images-rm: ## [DOCKER] Eliminar todas las imágenes del proyecto
	@echo "$(YELLOW)Eliminando imágenes...$(NC)"
	docker rmi $$(docker images -q '$(PROJECT_NAME)/*') 2>/dev/null || true

docker-volumes-ls: ## [DOCKER] Listar volúmenes del proyecto
	docker volume ls | grep $(PROJECT_NAME)

docker-volumes-rm: ## [DOCKER] Eliminar volúmenes del proyecto
	@echo "$(RED)⚠️  Esto eliminará todos los datos$(NC)"
	@read -p "¿Continuar? [y/N]: " confirm && [ "$$confirm" = "y" ] || exit 1
	docker volume rm $$(docker volume ls -q | grep $(PROJECT_NAME)) 2>/dev/null || true

# =============================================================================
# 🌐 NETWORKING - DIAGNÓSTICO
# =============================================================================

network-ls: ## [NETWORK] Listar redes del proyecto
	@echo "$(CYAN)Redes del proyecto:$(NC)"
	docker network ls | grep $(PROJECT_NAME)

network-inspect: ## [NETWORK] Inspeccionar red (uso: make network-inspect NET=frontend)
	@echo "$(CYAN)Inspeccionando red $(PROJECT_NAME)_$(NET):$(NC)"
	docker network inspect $(PROJECT_NAME)_$(NET) | jq .

network-containers: ## [NETWORK] Ver containers por red
	@for network in $$(docker network ls --filter "name=$(PROJECT_NAME)" --format "{{.Name}}"); do \
		echo "$(CYAN)$$network:$(NC)"; \
		docker network inspect $$network | jq -r '.[0].Containers | to_entries[] | "  - \(.value.Name) (\(.value.IPv4Address))"'; \
		echo ""; \
	done

network-test-dns: ## [NETWORK] Test DNS entre containers
	@echo "$(CYAN)Testeando DNS resolution...$(NC)"
	docker exec $(PROJECT_NAME)-api-1 nslookup postgres || true
	docker exec $(PROJECT_NAME)-api-1 nslookup react || true

network-test-ping: ## [NETWORK] Ping entre containers (uso: make network-test-ping FROM=api TO=postgres)
	@echo "$(CYAN)Ping desde $(FROM) a $(TO):$(NC)"
	docker exec $(PROJECT_NAME)-$(FROM)-1 ping -c 3 $(TO)

network-curl-test: ## [NETWORK] Test HTTP entre servicios
	@echo "$(CYAN)Test HTTP interno:$(NC)"
	@echo "API -> PostgreSQL: "
	docker exec $(PROJECT_NAME)-api-1 curl -s http://postgres:5432 || echo "No HTTP (esperado para DB)"

# =============================================================================
# ☸️  KUBERNETES - GESTIÓN
# =============================================================================

k8s-context: ## [K8S] Ver contexto actual
	kubectl config current-context

k8s-contexts: ## [K8S] Listar todos los contextos
	kubectl config get-contexts

k8s-use-minikube: ## [K8S] Cambiar a contexto minikube
	kubectl config use-context minikube

k8s-namespace-create: ## [K8S] Crear namespace del proyecto
	kubectl create namespace $(PROJECT_NAME) --dry-run=client -o yaml | kubectl apply -f -

k8s-apply-dev: ## [K8S] Aplicar manifests a staging
	kubectl apply -k kubernetes/overlays/staging

k8s-apply-prod: ## [K8S] Aplicar manifests a producción
	@echo "$(RED)⚠️  Deploy a PRODUCCIÓN$(NC)"
	@read -p "¿Confirmar? [y/N]: " confirm && [ "$$confirm" = "y" ] || exit 1
	kubectl apply -k kubernetes/overlays/production

k8s-delete: ## [K8S] Eliminar recursos del proyecto
	kubectl delete namespace $(PROJECT_NAME)

k8s-pods: ## [K8S] Listar pods del proyecto
	kubectl get pods -n $(PROJECT_NAME)

k8s-services: ## [K8S] Listar services
	kubectl get services -n $(PROJECT_NAME)

k8s-logs: ## [K8S] Ver logs (uso: make k8s-logs POD=api-xxx)
	kubectl logs -f $(POD) -n $(PROJECT_NAME)

k8s-describe: ## [K8S] Describir recurso (uso: make k8s-describe TYPE=pod NAME=api-xxx)
	kubectl describe $(TYPE) $(NAME) -n $(PROJECT_NAME)

k8s-shell: ## [K8S] Shell en pod (uso: make k8s-shell POD=api-xxx)
	kubectl exec -it $(POD) -n $(PROJECT_NAME) -- /bin/sh

k8s-port-forward-api: ## [K8S] Port forward API local
	kubectl port-forward -n $(PROJECT_NAME) service/api 8000:8000

k8s-port-forward-grafana: ## [K8S] Port forward Grafana local
	kubectl port-forward -n $(PROJECT_NAME) service/grafana 3001:3000

# =============================================================================
# 🔍 DEBUGGING - HEALTH CHECKS
# =============================================================================

health-all: ## [DEBUG] Verificar health de todos los servicios
	@echo "$(CYAN)Health Check de Servicios:$(NC)"
	@echo ""
	@echo -n "  API:        "
	@curl -sf http://localhost/api/health > /dev/null && echo "$(GREEN)✅ OK$(NC)" || echo "$(RED)❌ FAIL$(NC)"
	@echo -n "  Dash:       "
	@curl -sf http://localhost/dash > /dev/null && echo "$(GREEN)✅ OK$(NC)" || echo "$(RED)❌ FAIL$(NC)"
	@echo -n "  React:      "
	@curl -sf http://localhost > /dev/null && echo "$(GREEN)✅ OK$(NC)" || echo "$(RED)❌ FAIL$(NC)"
	@echo -n "  Prometheus: "
	@curl -sf http://localhost:9090/-/healthy > /dev/null && echo "$(GREEN)✅ OK$(NC)" || echo "$(RED)❌ FAIL$(NC)"
	@echo -n "  Grafana:    "
	@curl -sf http://localhost:3001/api/health > /dev/null && echo "$(GREEN)✅ OK$(NC)" || echo "$(RED)❌ FAIL$(NC)"
	@echo -n "  Loki:       "
	@curl -sf http://localhost:3100/ready > /dev/null && echo "$(GREEN)✅ OK$(NC)" || echo "$(RED)❌ FAIL$(NC)"
	@echo ""

health-db: ## [DEBUG] Verificar conexión a base de datos
	@echo "$(CYAN)Verificando PostgreSQL...$(NC)"
	docker exec $(PROJECT_NAME)-postgres-1 pg_isready -U mlp_user

debug-env: ## [DEBUG] Mostrar variables de entorno de un container
	@echo "$(CYAN)Variables de entorno (uso: make debug-env CONTAINER=api):$(NC)"
	docker exec $(PROJECT_NAME)-$(CONTAINER)-1 env

debug-disk: ## [DEBUG] Ver uso de disco en containers
	@echo "$(CYAN)Uso de disco en containers:$(NC)"
	@for container in $$(docker ps --filter "name=$(PROJECT_NAME)" --format "{{.Names}}"); do \
		echo "$(YELLOW)$$container:$(NC)"; \
		docker exec $$container df -h 2>/dev/null || echo "  No disponible"; \
	done

debug-ports: ## [DEBUG] Ver puertos en uso
	@echo "$(CYAN)Puertos mapeados:$(NC)"
	docker ps --filter "name=$(PROJECT_NAME)" --format "table {{.Names}}\t{{.Ports}}"

debug-traefik: ## [DEBUG] Ver configuración de Traefik
	@echo "$(CYAN)Traefik routers:$(NC)"
	@curl -s http://localhost:8080/api/http/routers | jq '.[] | {name: .name, rule: .rule, service: .service}'

# =============================================================================
# 🔍 DEBUGGING - LOGS AVANZADOS
# =============================================================================

logs-errors: ## [DEBUG] Buscar errores en logs
	@echo "$(CYAN)Buscando errores en logs...$(NC)"
	docker logs $(PROJECT_NAME)-api-1 2>&1 | grep -i error | tail -20

logs-grep: ## [DEBUG] Buscar en logs (uso: make logs-grep PATTERN="texto")
	@for container in $$(docker ps --filter "name=$(PROJECT_NAME)" --format "{{.Names}}"); do \
		echo "$(CYAN)$$container:$(NC)"; \
		docker logs $$container 2>&1 | grep -i "$(PATTERN)" | tail -10; \
	done

logs-since: ## [DEBUG] Logs desde timestamp (uso: make logs-since TIME="5m")
	docker logs --since $(TIME) $(PROJECT_NAME)-api-1

# =============================================================================
# 🎯 WORKFLOWS COMPLETOS
# =============================================================================

infra-full: ## Levantar infraestructura completa
	@echo "$(GREEN)🚀 Levantando infraestructura completa...$(NC)"
	@$(MAKE) -C .. dev-up
	@$(MAKE) monitoring-up
	@sleep 5
	@$(MAKE) health-all
	@echo "$(GREEN)✅ Infraestructura completa activa$(NC)"

infra-down: ## Detener toda la infraestructura
	@$(MAKE) monitoring-down
	@$(MAKE) -C .. dev-down
	@echo "$(GREEN)✅ Infraestructura detenida$(NC)"

# =============================================================================
# FIN DEL MAKEFILE
# =============================================================================
