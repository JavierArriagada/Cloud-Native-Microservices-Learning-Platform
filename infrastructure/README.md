# Infrastructure

Configuración de infraestructura y orquestación.

## Estructura

- **docker/** - Docker Compose files para desarrollo y producción
- **traefik/** - Configuración del API Gateway
- **prometheus/** - Configuración de métricas
- **grafana/** - Dashboards y configuración
- **loki/** - Configuración de logs centralizados
- **kubernetes/** - Manifests de Kubernetes
  - **base/** - Recursos base
  - **overlays/** - Configuraciones por ambiente (staging/production)

## Tecnologías

- Docker Compose para desarrollo local
- Traefik como API Gateway y reverse proxy
- Kubernetes para producción (GKE en GCP)
- Kustomize para gestión de manifests
