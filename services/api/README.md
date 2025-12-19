# FastAPI Backend

API REST asíncrona construida con FastAPI.

## Características

- ✅ Async/await con asyncpg
- ✅ Validación con Pydantic
- ✅ OpenAPI/Swagger automático
- ✅ Health checks
- ✅ Prometheus metrics
- ✅ SQL puro (sin ORM)
- ✅ Migraciones con Alembic

## Estructura

```
app/
├── main.py           # Entry point de la aplicación
├── config.py         # Configuración y settings
├── database.py       # Conexión a PostgreSQL
├── models/           # Pydantic schemas (NO ORM models)
├── queries/          # SQL queries puro
├── schemas/          # Esquemas de request/response
├── routers/          # Endpoints organizados por recurso
└── services/         # Lógica de negocio
```

## Endpoints principales

- `GET /health` - Health check
- `GET /ready` - Readiness (incluye verificación de DB)
- `GET /metrics` - Métricas de Prometheus
- `GET /docs` - Documentación Swagger UI
- `GET /redoc` - Documentación ReDoc

## Desarrollo

```bash
# Levantar servicio en desarrollo
make dev-up

# Ver logs
make dev-logs-api

# Ejecutar tests
make test-api

# Lint
make lint-api

# Shell en container
make dev-shell-api
```

## Base de datos

Este servicio usa:
- **asyncpg** para queries SQL puro
- **Alembic** para migraciones
- **NO usa ORM** - todas las queries son SQL explícito

## Próximos pasos

- [ ] Crear `main.py` con FastAPI app
- [ ] Configurar `database.py` con pool de conexiones
- [ ] Implementar endpoint `/health`
- [ ] Configurar Alembic
- [ ] Crear Dockerfile
