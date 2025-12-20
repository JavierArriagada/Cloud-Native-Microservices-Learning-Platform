# Credenciales y Acceso a Servicios - Ambiente de Desarrollo

Este documento contiene las credenciales por defecto y guías de acceso para todos los servicios del proyecto en ambiente de desarrollo.

> **IMPORTANTE**: Estas credenciales son SOLO para desarrollo local. NUNCA uses estas credenciales en producción.

## Índice
- [URLs de Acceso](#urls-de-acceso)
- [Base de Datos PostgreSQL](#base-de-datos-postgresql)
- [Administrador de Base de Datos (Adminer)](#administrador-de-base-de-datos-adminer)
- [Grafana](#grafana)
- [Prometheus](#prometheus)
- [Loki](#loki)
- [FastAPI](#fastapi)

---

## URLs de Acceso

### Servicios Frontend y Gateway
| Servicio | URL | Descripción |
|----------|-----|-------------|
| React App | http://localhost | Aplicación web principal |
| Traefik Dashboard | http://localhost:8080 | Panel de control del API Gateway |

### Servicios Backend
| Servicio | URL | Descripción |
|----------|-----|-------------|
| FastAPI | http://localhost/api | API REST principal |
| FastAPI Docs | http://localhost/api/docs | Documentación interactiva (Swagger) |
| Dash Dashboard | http://localhost/dash | Dashboard de análisis |

### Base de Datos
| Servicio | URL/Puerto | Descripción |
|----------|------------|-------------|
| PostgreSQL | localhost:5432 | Base de datos principal |
| Adminer | http://localhost/database | Interfaz web de administración |

### Monitoreo
| Servicio | URL | Descripción |
|----------|-----|-------------|
| Prometheus | http://localhost/prometheus | Sistema de métricas y alertas |
| Grafana | http://localhost/grafana | Visualización de métricas |
| Loki API | http://localhost/loki | API de agregación de logs |

### Acceso Directo (sin proxy de Traefik)
| Servicio | URL |
|----------|-----|
| Prometheus | http://localhost:9090 |
| Grafana | http://localhost:3001 |
| Loki | http://localhost:3100 |

---

## Base de Datos PostgreSQL

### Credenciales
```
Host:     postgres (desde contenedores) / localhost (desde host)
Puerto:   5432
Database: mlp_db
Usuario:  mlp_user
Password: mlp_secret_change_in_production
```

### Conexión desde Host (tu máquina)
```bash
psql -h localhost -p 5432 -U mlp_user -d mlp_db
# Password: mlp_secret_change_in_production
```

### String de Conexión
```
postgresql://mlp_user:mlp_secret_change_in_production@localhost:5432/mlp_db
```

### Conexión desde Python
```python
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="mlp_db",
    user="mlp_user",
    password="mlp_secret_change_in_production"
)
```

---

## Administrador de Base de Datos (Adminer)

### Acceso
URL: **http://localhost/database**

### Credenciales de Login
```
Sistema:    PostgreSQL
Servidor:   postgres
Usuario:    mlp_user
Contraseña: mlp_secret_change_in_production
Base datos: mlp_db
```

### Pasos para entrar:
1. Abre http://localhost/database en tu navegador
2. Selecciona **PostgreSQL** en el campo "Sistema"
3. Completa los campos:
   - **Servidor**: `postgres`
   - **Usuario**: `mlp_user`
   - **Contraseña**: `mlp_secret_change_in_production`
   - **Base de datos**: `mlp_db` (opcional, puedes dejarlo vacío)
4. Click en **Entrar**

### Características de Adminer
- Explorar tablas y esquemas
- Ejecutar queries SQL
- Importar/exportar datos
- Crear y modificar tablas
- Ver relaciones entre tablas
- Gestionar usuarios y permisos

---

## Grafana

### Acceso
URL: **http://localhost/grafana**

### Credenciales por Defecto
```
Usuario:    admin
Contraseña: admin_change_in_production
```

### Pasos para entrar:
1. Abre http://localhost/grafana en tu navegador
2. En la pantalla de login ingresa:
   - **Email or username**: `admin`
   - **Password**: `admin_change_in_production`
3. Click en **Log in**
4. (Opcional) Grafana te pedirá cambiar la contraseña en el primer login, puedes omitir este paso en desarrollo

### Configuración Inicial

#### Agregar Prometheus como Data Source
1. Ve a **Configuration** → **Data Sources**
2. Click en **Add data source**
3. Selecciona **Prometheus**
4. Configura:
   - **Name**: Prometheus
   - **URL**: `http://mlp_prometheus:9090`
5. Click en **Save & Test**

#### Agregar Loki como Data Source
1. Ve a **Configuration** → **Data Sources**
2. Click en **Add data source**
3. Selecciona **Loki**
4. Configura:
   - **Name**: Loki
   - **URL**: `http://mlp_loki:3100`
5. Click en **Save & Test**

### Dashboards Recomendados
- **Prometheus Stats**: Métricas del sistema
- **Loki Logs**: Visualización de logs
- Puedes importar dashboards desde https://grafana.com/grafana/dashboards/

---

## Prometheus

### Acceso
URL: **http://localhost/prometheus**

### Características
- No requiere autenticación en desarrollo
- Interfaz de consultas PromQL
- Visualización de métricas en tiempo real
- Configuración de alertas

### Acceso Directo (sin Traefik)
URL: **http://localhost:9090**

### Ejemplos de Queries
```promql
# CPU usage
rate(process_cpu_seconds_total[5m])

# Memory usage
process_resident_memory_bytes

# HTTP requests
rate(http_requests_total[5m])
```

### Targets Configurados
Ve a http://localhost/prometheus/targets para ver todos los endpoints que Prometheus está monitoreando.

---

## Loki

### Acceso
**IMPORTANTE**: Loki NO tiene interfaz web de usuario. Es una API de agregación de logs.

### ¿Por qué obtengo 404?
Loki es un servicio backend que solo expone endpoints API. Para visualizar logs, debes usar:
- **Grafana** (recomendado): http://localhost/grafana
- **LogCLI**: Herramienta de línea de comandos

### Acceso a la API
```bash
# Verificar que Loki está funcionando
curl http://localhost/loki/ready

# Verificar métricas
curl http://localhost/loki/metrics

# Query de logs (requiere parámetros específicos)
curl -G -s "http://localhost/loki/loki/api/v1/query" --data-urlencode 'query={job="varlogs"}'
```

### Ver Logs en Grafana
1. Accede a Grafana: http://localhost/grafana
2. Agrega Loki como Data Source (ver sección de Grafana)
3. Ve a **Explore**
4. Selecciona **Loki** como data source
5. Usa el query builder para filtrar logs

### Acceso Directo (sin Traefik)
URL: **http://localhost:3100**

---

## FastAPI

### Acceso
- **API Base**: http://localhost/api
- **Documentación Swagger**: http://localhost/api/docs
- **Documentación ReDoc**: http://localhost/api/redoc

### Endpoints Principales
```
GET  /api/health          - Health check
GET  /api/                - Root endpoint
GET  /api/docs            - Documentación interactiva
GET  /api/redoc           - Documentación alternativa
```

### Probar la API
```bash
# Health check
curl http://localhost/api/health

# Ejemplo de endpoint (ajustar según tu API)
curl http://localhost/api/users
```

---

## Variables de Entorno

Todas estas credenciales están configuradas en el archivo `.env` en la raíz del proyecto.

### Cambiar Credenciales
1. Edita el archivo `.env`
2. Modifica las variables correspondientes
3. Reinicia los servicios:
   ```bash
   make restart
   # o
   docker compose down && docker compose up -d
   ```

### Variables Importantes
```bash
# PostgreSQL
POSTGRES_USER=mlp_user
POSTGRES_PASSWORD=mlp_secret_change_in_production
POSTGRES_DB=mlp_db

# Grafana
GRAFANA_ADMIN_USER=admin
GRAFANA_ADMIN_PASSWORD=admin_change_in_production

# API Security
API_SECRET_KEY=super-secret-key-change-in-production-min-32-chars
```

---

## Troubleshooting

### No puedo conectarme a PostgreSQL
- Verifica que el contenedor esté corriendo: `docker ps | grep postgres`
- Verifica los logs: `docker logs mlp_postgres`
- Asegúrate de usar `localhost` desde tu máquina y `postgres` desde otros contenedores

### Adminer no carga
- Verifica que estés usando `postgres` como servidor (no `localhost`)
- Revisa los logs de Traefik: `docker logs mlp_traefik`
- Verifica que el contenedor de Adminer esté corriendo: `docker ps | grep adminer`

### Grafana no acepta mis credenciales
- Verifica las credenciales en el archivo `.env`
- Resetea Grafana eliminando el volumen:
  ```bash
  docker compose down
  docker volume rm mlp_grafana_data
  docker compose up -d
  ```

### Loki muestra 404
- Esto es NORMAL. Loki no tiene interfaz web
- Usa Grafana para visualizar logs
- O usa la API directamente con curl

---

## Seguridad en Desarrollo

### Credenciales por Defecto
Estas credenciales son intencionalmente débiles para facilitar el desarrollo local. Los nombres incluyen `_change_in_production` como recordatorio.

### NUNCA en Producción
- Cambia TODAS las credenciales antes de desplegar a producción
- Usa secretos de Docker/Kubernetes en producción
- Habilita HTTPS/TLS en producción
- Implementa autenticación y autorización robustas

### Buenas Prácticas
1. No commits el archivo `.env` al repositorio (ya está en `.gitignore`)
2. Usa `.env.example` como plantilla para otros desarrolladores
3. Documenta cualquier cambio de credenciales con el equipo
4. Usa gestores de secretos (Vault, AWS Secrets Manager, etc.) en producción

---

## Resumen Rápido

| Servicio | URL | Usuario | Contraseña |
|----------|-----|---------|------------|
| Adminer | http://localhost/database | mlp_user | mlp_secret_change_in_production |
| Grafana | http://localhost/grafana | admin | admin_change_in_production |
| PostgreSQL | localhost:5432 | mlp_user | mlp_secret_change_in_production |
| Prometheus | http://localhost/prometheus | - | - |
| Loki | http://localhost/loki (API) | - | - |

---

**Última actualización**: 2025-12-19
**Ambiente**: Desarrollo Local
**Versión del proyecto**: 1.0.0
