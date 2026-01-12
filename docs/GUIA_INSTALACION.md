# 🚀 Guía de Instalación - Cloud-Native Microservices Learning Platform

Esta guía te llevará paso a paso por el proceso de instalación del proyecto en tu máquina local.

---

## 📋 Tabla de Contenidos

1. [Requisitos Previos](#-requisitos-previos)
2. [Instalación Rápida](#-instalación-rápida)
3. [Instalación Paso a Paso](#-instalación-paso-a-paso)
4. [Verificación de la Instalación](#-verificación-de-la-instalación)
5. [Solución de Problemas](#-solución-de-problemas)
6. [Próximos Pasos](#-próximos-pasos)

---

## 📦 Requisitos Previos

### Software Requerido

Antes de comenzar, asegúrate de tener instalado lo siguiente:

#### 1. **Docker Desktop** (Requerido)
- **Versión mínima**: 20.10+
- **Descarga**: https://www.docker.com/products/docker-desktop
- **Incluye**: Docker Engine + Docker Compose v2

**Verificar instalación:**
```bash
docker --version
# Debería mostrar: Docker version 20.10.x o superior

docker compose version
# Debería mostrar: Docker Compose version v2.x.x
```

#### 2. **Git** (Requerido)
- **Versión mínima**: 2.30+
- **Descarga**: https://git-scm.com/downloads

**Verificar instalación:**
```bash
git --version
# Debería mostrar: git version 2.30.x o superior
```

#### 3. **Make** (Recomendado)
- **Linux/macOS**: Generalmente preinstalado
- **Windows**: Instalar via [Chocolatey](https://chocolatey.org/) o [Git Bash](https://gitforwindows.org/)

**Verificar instalación:**
```bash
make --version
# Debería mostrar: GNU Make 3.81 o superior
```

### Herramientas Opcionales (Para Desarrollo Local)

Estas herramientas solo son necesarias si quieres ejecutar servicios fuera de Docker:

- **Python 3.12+**: Para desarrollo local del API y Dash
- **Node.js 18+**: Para desarrollo local del frontend React
- **psql** (PostgreSQL Client): Para acceso directo a la base de datos

---

## ⚡ Instalación Rápida

Si ya tienes todos los requisitos instalados, puedes levantar el proyecto en 3 comandos:

```bash
# 1. Clonar el repositorio
git clone https://github.com/JavierArriagada/Cloud-Native-Microservices-Learning-Platform.git
cd Cloud-Native-Microservices-Learning-Platform

# 2. Configurar variables de entorno
cp .env.example .env

# 3. Levantar todos los servicios
docker compose -f infrastructure/docker/docker-compose.yml -f infrastructure/docker/docker-compose.dev.yml up -d

# 4. Aplicar migraciones de base de datos
docker exec -it mlp-api-1 python -m alembic upgrade head

# 5. Cargar datos de ejemplo (opcional)
docker exec -it mlp-api-1 python -m scripts.seed_data
```

**¡Listo!** Accede a http://localhost para ver la aplicación.

---

## 🔧 Instalación Paso a Paso

### Paso 1: Clonar el Repositorio

```bash
# Clonar el proyecto
git clone https://github.com/JavierArriagada/Cloud-Native-Microservices-Learning-Platform.git

# Entrar al directorio
cd Cloud-Native-Microservices-Learning-Platform

# Verificar que estás en el directorio correcto
ls -la
# Deberías ver: README.md, services/, infrastructure/, docs/, etc.
```

---

### Paso 2: Configurar Variables de Entorno

El proyecto utiliza variables de entorno para configurar servicios, credenciales y puertos.

```bash
# Copiar el archivo de ejemplo
cp .env.example .env

# Abrir el archivo para editarlo (opcional)
nano .env
# O usa tu editor favorito: code .env, vim .env, etc.
```

**Configuración por defecto (para desarrollo local):**

Las configuraciones por defecto funcionan sin modificaciones. Sin embargo, puedes personalizar:

```env
# Base de datos PostgreSQL
POSTGRES_DB=mlp_db
POSTGRES_USER=mlp_user
POSTGRES_PASSWORD=mlp_secret_change_in_production

# API Secret (cambiar en producción)
API_SECRET_KEY=super-secret-key-change-in-production-min-32-chars

# Puertos (si hay conflictos en tu máquina)
TRAEFIK_HTTP_PORT=80
GRAFANA_PORT=3001
PROMETHEUS_PORT=9090
```

⚠️ **Importante**: Las contraseñas por defecto son solo para desarrollo. **Cámbialas en producción**.

---

### Paso 3: Verificar Docker

Antes de levantar los servicios, verifica que Docker esté funcionando:

```bash
# Verificar que Docker está corriendo
docker info

# Si obtienes un error, inicia Docker Desktop
# Linux: sudo systemctl start docker
# macOS/Windows: Abre Docker Desktop
```

---

### Paso 4: Construir las Imágenes Docker

```bash
# Construir todas las imágenes
docker compose -f infrastructure/docker/docker-compose.yml -f infrastructure/docker/docker-compose.dev.yml build

# Esto tomará varios minutos la primera vez
# Verás mensajes de descarga de dependencias para:
# - FastAPI (Python)
# - Dash (Python)
# - React (Node.js)
```

**Progreso esperado:**
```
[+] Building 125.4s (45/45) FINISHED
 => [api internal] load build definition
 => [dash internal] load build definition
 => [react internal] load build definition
 ...
```

---

### Paso 5: Levantar los Servicios

```bash
# Opción A: Usar Docker Compose directamente
docker compose -f infrastructure/docker/docker-compose.yml -f infrastructure/docker/docker-compose.dev.yml up -d

# Opción B: Usar Makefile (si tienes Make instalado)
make dev-up
```

**Flags explicados:**
- `-f infrastructure/docker/docker-compose.yml`: Archivo base de producción
- `-f infrastructure/docker/docker-compose.dev.yml`: Sobrescribe configuraciones para desarrollo
- `-d`: Modo detached (segundo plano)

**Servicios que se levantarán:**
```
✔ Network mlp_frontend    Created
✔ Network mlp_backend     Created
✔ Network mlp_monitoring  Created
✔ Container mlp-postgres-1  Started
✔ Container mlp-api-1       Started
✔ Container mlp-dash-1      Started
✔ Container mlp-react-1     Started
✔ Container mlp-traefik-1   Started
✔ Container mlp-prometheus-1 Started
✔ Container mlp-grafana-1    Started
```

---

### Paso 6: Verificar Estado de los Servicios

```bash
# Ver estado de todos los contenedores
docker compose -f infrastructure/docker/docker-compose.yml -f infrastructure/docker/docker-compose.dev.yml ps

# O con Makefile
make dev-status
```

**Estado esperado (todos deben estar "Up"):**
```
NAME                 IMAGE                          STATUS
mlp-api-1           mlp-api:dev                    Up (healthy)
mlp-dash-1          mlp-dash:dev                   Up (healthy)
mlp-postgres-1      postgres:16-alpine             Up (healthy)
mlp-react-1         mlp-react:dev                  Up
mlp-traefik-1       traefik:v3.0                   Up (healthy)
mlp-grafana-1       grafana/grafana:latest         Up
mlp-prometheus-1    prom/prometheus:latest         Up
```

---

### Paso 7: Aplicar Migraciones de Base de Datos

La base de datos necesita ser inicializada con el esquema correcto:

```bash
# Ejecutar migraciones de Alembic
docker exec -it mlp-api-1 python -m alembic upgrade head

# O entrar al contenedor y ejecutar manualmente
docker exec -it mlp-api-1 bash
python -m alembic upgrade head
exit
```

**Salida esperada:**
```
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade -> abc123, Initial tables
INFO  [alembic.runtime.migration] Running upgrade abc123 -> def456, Add audit logs
```

---

### Paso 8: Cargar Datos de Ejemplo (Opcional)

Para probar la aplicación con datos de ejemplo:

```bash
# Cargar datos básicos (usuarios, roles)
docker exec -it mlp-api-1 python -m scripts.seed_data

# Cargar datos del dominio de minería
docker exec -it mlp-api-1 python -m scripts.seed_mining_data
```

**Datos que se crearán:**
- 3 roles: Admin, Manager, User
- 5 usuarios de ejemplo
- Equipos y yacimientos mineros
- Registros de auditoría de ejemplo

---

### Paso 9: Verificar Logs

Revisa que no haya errores en los logs:

```bash
# Ver logs de todos los servicios
docker compose -f infrastructure/docker/docker-compose.yml -f infrastructure/docker/docker-compose.dev.yml logs

# Ver logs de un servicio específico
docker logs mlp-api-1
docker logs mlp-postgres-1

# Seguir logs en tiempo real
docker logs -f mlp-api-1
```

---

## ✅ Verificación de la Instalación

### Acceso a Servicios

Abre tu navegador y verifica que todos los servicios respondan:

| Servicio | URL | Credenciales | Estado Esperado |
|----------|-----|--------------|-----------------|
| **Frontend React** | http://localhost | - | Aplicación web cargada |
| **FastAPI Backend** | http://localhost/api | - | `{"message": "API running"}` |
| **FastAPI Docs** | http://localhost/api/docs | - | Documentación Swagger |
| **Dash Dashboard** | http://localhost/dash | - | Dashboard interactivo |
| **Traefik Dashboard** | http://localhost:8080 | admin/admin | Panel de Traefik |
| **Grafana** | http://localhost:3001 | admin/admin_change_in_production | Dashboards de monitoreo |
| **Prometheus** | http://localhost:9090 | - | Interfaz de métricas |

### Test de Conectividad

```bash
# Test del API
curl http://localhost/api/health
# Esperado: {"status": "healthy"}

# Test de base de datos
docker exec -it mlp-postgres-1 psql -U mlp_user -d mlp_db -c "SELECT version();"
# Esperado: PostgreSQL 16.x
```

### Verificación de Base de Datos

```bash
# Listar tablas creadas
docker exec -it mlp-postgres-1 psql -U mlp_user -d mlp_db -c "\dt"

# Esperado:
#  Schema |     Name     | Type  |   Owner
# --------+--------------+-------+-----------
#  public | users        | table | mlp_user
#  public | roles        | table | mlp_user
#  public | user_roles   | table | mlp_user
#  public | sessions     | table | mlp_user
#  public | audit_logs   | table | mlp_user
```

---

## 🛑 Detener los Servicios

```bash
# Detener todos los servicios (mantiene datos)
docker compose -f infrastructure/docker/docker-compose.yml -f infrastructure/docker/docker-compose.dev.yml down

# O con Makefile
make dev-down

# Detener y eliminar volúmenes (⚠️ borra la base de datos)
docker compose -f infrastructure/docker/docker-compose.yml -f infrastructure/docker/docker-compose.dev.yml down -v
```

---

## 🔧 Solución de Problemas

### Problema 1: Puerto ya en uso

**Error:**
```
Error response from daemon: Ports are not available: exposing port TCP 0.0.0.0:80 -> 0.0.0.0:0: listen tcp 0.0.0.0:80: bind: address already in use
```

**Solución:**
```bash
# Ver qué proceso está usando el puerto 80
sudo lsof -i :80
# O en Windows: netstat -ano | findstr :80

# Detener el servicio conflictivo o cambiar el puerto en .env
TRAEFIK_HTTP_PORT=8080  # Usar otro puerto
```

### Problema 2: Docker no está corriendo

**Error:**
```
Cannot connect to the Docker daemon at unix:///var/run/docker.sock
```

**Solución:**
```bash
# Linux
sudo systemctl start docker
sudo systemctl enable docker

# macOS/Windows
# Abre Docker Desktop manualmente
```

### Problema 3: Migraciones fallan

**Error:**
```
sqlalchemy.exc.OperationalError: could not connect to server
```

**Solución:**
```bash
# Esperar a que PostgreSQL esté listo (puede tomar 10-30 segundos)
docker exec -it mlp-postgres-1 pg_isready -U mlp_user

# Si el contenedor no está sano, reiniciarlo
docker restart mlp-postgres-1

# Esperar 20 segundos y volver a intentar las migraciones
sleep 20
docker exec -it mlp-api-1 python -m alembic upgrade head
```

### Problema 4: Permisos de archivos (Linux)

**Error:**
```
Permission denied: '/app/...'
```

**Solución:**
```bash
# Dar permisos al usuario actual
sudo chown -R $USER:$USER .

# O ejecutar Docker sin sudo (agregar usuario al grupo docker)
sudo usermod -aG docker $USER
newgrp docker
```

### Problema 5: Contenedores no levantan

**Diagnóstico:**
```bash
# Ver logs detallados
docker logs mlp-api-1 --tail 100

# Ver estado de salud
docker inspect mlp-api-1 | grep -A 10 Health

# Reconstruir imagen desde cero
docker compose -f infrastructure/docker/docker-compose.yml -f infrastructure/docker/docker-compose.dev.yml build --no-cache api
```

---

## 🎯 Próximos Pasos

Una vez que la instalación esté completa y verificada:

### 1. Explorar la Documentación

- **[Guía de Base de Datos](DATABASE_GUIDE.md)**: Aprende sobre el esquema y cómo crear tablas
- **[Workflow de Desarrollo](CLAUDE_CODE_WORKFLOW.md)**: Mejores prácticas para desarrollo
- **[Credenciales](DEVELOPMENT_CREDENTIALS.md)**: Usuarios y contraseñas por defecto

### 2. Desarrollo Local

```bash
# Si prefieres trabajar sin Docker (requiere Python 3.12+)
cd services/api
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 3. Comandos Útiles con Makefile

```bash
# Ver todos los comandos disponibles
make help

# Comandos frecuentes
make dev-up           # Levantar servicios
make dev-down         # Detener servicios
make dev-logs         # Ver logs en tiempo real
make dev-restart      # Reiniciar todos los servicios
make db-migrate       # Aplicar migraciones
make db-seed          # Cargar datos de ejemplo
make test             # Ejecutar tests
make lint             # Verificar código
```

### 4. Crear Nueva Funcionalidad

```bash
# Crear una nueva tabla en la base de datos
./services/api/scripts/create_table.sh

# Ver guía completa
cat docs/DATABASE_NEW_TABLE_GUIDE.md
```

### 5. Monitoreo y Debugging

- **Grafana** (http://localhost:3001): Ver métricas en tiempo real
- **Traefik** (http://localhost:8080): Monitorear enrutamiento de requests
- **Prometheus** (http://localhost:9090): Consultar métricas directamente

---

## 📚 Recursos Adicionales

- [README Principal](../README.md)
- [Documentación Completa](README.md)
- [Planificación y Arquitectura](MICROSERVICES_MASTER_PLAN.md)
- [Configuración de Traefik](TRAEFIK_ROUTING_CONFIG.md)

---

## 💬 Soporte

Si encuentras problemas durante la instalación:

1. Revisa la sección de [Solución de Problemas](#-solución-de-problemas)
2. Consulta los logs: `docker compose logs`
3. Abre un issue en GitHub con los detalles del error

---

## 📝 Checklist de Instalación

Usa este checklist para verificar que completaste todos los pasos:

- [ ] Docker y Docker Compose instalados
- [ ] Git instalado
- [ ] Repositorio clonado
- [ ] Archivo `.env` configurado
- [ ] Imágenes Docker construidas
- [ ] Servicios levantados (todos en estado "Up")
- [ ] Migraciones de base de datos aplicadas
- [ ] Datos de ejemplo cargados (opcional)
- [ ] Frontend accesible en http://localhost
- [ ] API Docs accesible en http://localhost/api/docs
- [ ] Base de datos conecta correctamente

---

**¡Felicitaciones! 🎉** Has instalado exitosamente la Cloud-Native Microservices Learning Platform.

Ahora puedes empezar a desarrollar, aprender sobre microservicios, y experimentar con arquitecturas cloud-native.
