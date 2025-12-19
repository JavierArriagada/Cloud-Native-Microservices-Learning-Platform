# Docker Compose Configurations

Archivos de Docker Compose para diferentes entornos.

## Archivos

- **docker-compose.yml** - Configuración base de servicios
- **docker-compose.dev.yml** - Overrides para desarrollo (hot reload, debug)
- **docker-compose.monitoring.yml** - Stack de monitoreo (Prometheus, Grafana, Loki)

## Uso

```bash
# Desarrollo (compose.yml + compose.dev.yml)
make dev-up

# Solo monitoreo
make monitoring-up

# Producción (solo compose.yml)
docker compose -f docker-compose.yml up -d
```

## Servicios planeados

### Aplicación
- **postgres** - PostgreSQL 16
- **api** - FastAPI backend
- **dash** - Dash dashboard
- **react** - React frontend
- **traefik** - API Gateway

### Monitoreo
- **prometheus** - Métricas
- **grafana** - Visualización
- **loki** - Logs
- **promtail** - Log collector

## Redes

- **frontend** - Traefik, React, Dash
- **backend** - API, PostgreSQL
- **monitoring** - Prometheus, Grafana, Loki

## Próximos pasos

- [ ] Crear docker-compose.yml
- [ ] Crear docker-compose.dev.yml
- [ ] Crear docker-compose.monitoring.yml
