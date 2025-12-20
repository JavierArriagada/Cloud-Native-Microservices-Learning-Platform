# 🚀 Guía de Setup de Base de Datos

## Instrucciones Paso a Paso para Configurar la Base de Datos

**Fecha:** 2025-12-19
**Versión:** 1.0.0

---

## 📋 Pre-requisitos

✅ Servicios corriendo:
```bash
make dev-up
```

Verifica que estén corriendo:
- PostgreSQL (mlp_postgres)
- API (mlp_api)
- Adminer (mlp_adminer)

---

## 🔄 Paso 1: Rebuild del Contenedor API

Como agregamos nuevas dependencias (SQLAlchemy), necesitas hacer rebuild:

```bash
# Detener servicios
make dev-down

# Rebuild API container con nuevas dependencias
make build-api

# Levantar servicios nuevamente
make dev-up
```

**¿Por qué?** Agregamos `sqlalchemy==2.0.25` en requirements.txt para Alembic.

---

## 🗄️ Paso 2: Generar Primera Migración

Ahora que el container está rebuildeado, vamos a generar la primera migración con todas las tablas:

```bash
# Generar migration automáticamente
make db-migrate-create MSG="initial schema with users roles sessions"
```

**Esto hará:**
1. Alembic comparará los modelos SQLAlchemy en `app/db_models/` con la DB vacía
2. Generará un archivo de migración en `services/api/alembic/versions/`
3. El archivo contendrá `CREATE TABLE` para: users, roles, user_roles, sessions

**Ejemplo de output:**
```
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.autogenerate.compare] Detected added table 'roles'
INFO  [alembic.autogenerate.compare] Detected added table 'users'
INFO  [alembic.autogenerate.compare] Detected added table 'sessions'
INFO  [alembic.autogenerate.compare] Detected added table 'user_roles'
  Generating /app/alembic/versions/abc123def456_initial_schema_with_users_roles_sessions.py ...  done
```

---

## ✅ Paso 3: Revisar la Migración Generada

**IMPORTANTE:** SIEMPRE revisar migrations antes de aplicar.

```bash
# Ver el archivo generado (reemplaza abc123... con tu ID real)
cat services/api/alembic/versions/abc123*_initial_schema*.py
```

Verifica que contenga:
- ✅ `op.create_table('users', ...)`
- ✅ `op.create_table('roles', ...)`
- ✅ `op.create_table('user_roles', ...)`
- ✅ `op.create_table('sessions', ...)`
- ✅ Todos los índices y constraints
- ✅ Función `downgrade()` que elimina las tablas

---

## 🚀 Paso 4: Aplicar la Migración

Una vez revisada, aplicar la migración:

```bash
make db-migrate
```

**Output esperado:**
```
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> abc123def456, initial schema with users roles sessions
```

---

## 🌱 Paso 5: Poblar Datos Iniciales (Seed)

Ahora vamos a crear los roles del sistema y el usuario administrador:

```bash
make db-seed
```

**Esto creará:**
- 4 roles: `ADMIN`, `MODERATOR`, `USER`, `GUEST`
- 1 usuario administrador:
  - Email: `admin@example.com`
  - Password: `Admin123!`
  - Rol: `ADMIN`

**Output esperado:**
```
======================================================================
  🌱 SEED DATA - Cloud Native Microservices Learning Platform
======================================================================

📡 Conectando a base de datos...
✅ Conexión establecida

📝 Creando roles del sistema...
  ✅ Rol creado: ADMIN (prioridad: 1000)
  ✅ Rol creado: MODERATOR (prioridad: 500)
  ✅ Rol creado: USER (prioridad: 100)
  ✅ Rol creado: GUEST (prioridad: 10)
✅ 4 roles creados

👤 Creando usuario administrador por defecto...
  ✅ Usuario admin creado: admin@example.com
     Username: admin
     Password: Admin123! (¡CAMBIAR EN PRODUCCIÓN!)

🔑 Asignando rol ADMIN...
  ✅ Rol ADMIN asignado al usuario administrador

======================================================================
  ✅ Seed data completado exitosamente
======================================================================

Credenciales de administrador:
  Email:    admin@example.com
  Password: Admin123!

⚠️  IMPORTANTE: Cambiar password en producción!
```

---

## 🔍 Paso 6: Verificar la Base de Datos

### Opción A: Usar Adminer (Recomendado - Interfaz Gráfica)

1. Abrir navegador en: **http://localhost/database**
2. Login:
   - Sistema: `PostgreSQL`
   - Servidor: `postgres`
   - Usuario: `mlp_user`
   - Password: `mlp_secret` (o el valor en tu .env)
   - Base de datos: `mlp_db`
3. Explorar las tablas creadas

### Opción B: Usar psql (Terminal)

```bash
# Conectar a PostgreSQL via psql
make db-shell

# Una vez dentro de psql:
# Ver todas las tablas
\dt

# Resultado esperado:
#  Schema |      Name       | Type  |  Owner
# --------+-----------------+-------+----------
#  public | alembic_version | table | mlp_user
#  public | roles           | table | mlp_user
#  public | sessions        | table | mlp_user
#  public | user_roles      | table | mlp_user
#  public | users           | table | mlp_user

# Ver estructura de tabla users
\d users

# Ver datos en tabla roles
SELECT * FROM roles;

# Salir
\q
```

---

## 📊 Paso 7: Verificar Historial de Migraciones

```bash
# Ver historial de migrations
make db-migrate-history

# Output:
# <base> -> abc123def456 (head), initial schema with users roles sessions
```

```bash
# Ver migration actual aplicada
docker compose exec api alembic current -v

# Output:
# abc123def456 (head), initial schema with users roles sessions
```

---

## 🎯 Siguiente Paso: Configurar Monitoreo de DB

Ahora que la base de datos está configurada, el siguiente paso es agregar monitoreo con Prometheus.

### Lo que falta:

**1. Configurar postgres_exporter** (métricas básicas de PostgreSQL):
- Conexiones activas
- Queries por segundo
- Tamaño de base de datos
- Uptime

**2. Dashboard de Grafana** para visualizar métricas de DB

---

## 🧪 Comandos Útiles para Testing

### Probar Queries SQL

```bash
# Conectar a DB
make db-shell

# Crear un usuario de prueba
INSERT INTO users (email, username, password_hash, first_name, last_name)
VALUES ('test@example.com', 'testuser', '$2b$12$hash', 'Test', 'User')
RETURNING *;

# Obtener usuario con sus roles
SELECT
    u.email,
    u.username,
    r.name as role
FROM users u
LEFT JOIN user_roles ur ON u.id = ur.user_id
LEFT JOIN roles r ON ur.role_id = r.id
WHERE u.email = 'admin@example.com';

# Ver todas las sesiones activas
SELECT
    s.id,
    u.email,
    s.created_at,
    s.expires_at
FROM sessions s
JOIN users u ON s.user_id = u.id
WHERE s.revoked_at IS NULL;
```

### Limpiar y Reiniciar DB (PELIGRO!)

```bash
# Reset completo de base de datos
make db-reset

# Esto hará:
# 1. Detener servicios
# 2. Eliminar volumes (borra TODOS los datos)
# 3. Levantar PostgreSQL
# 4. Aplicar migrations desde cero
```

### Revertir Migration

```bash
# Revertir última migration
make db-migrate-down

# Re-aplicar
make db-migrate
```

---

## 📚 Documentación Relacionada

| Documento | Descripción |
|-----------|-------------|
| `docs/DATABASE_SCHEMA_DESIGN.md` | Diseño completo del esquema de DB |
| `docs/ALEMBIC_GUIDE.md` | Guía completa de Alembic |
| `docs/DEPLOYMENT_STATUS.md` | Estado de servicios |
| `Makefile` | Todos los comandos disponibles |

---

## 🆘 Troubleshooting

### Error: "sqlalchemy" module not found

**Solución:**
```bash
make dev-down
make build-api  # Rebuild con nuevas dependencias
make dev-up
```

### Error: "Can't locate revision"

**Solución:**
```bash
git pull  # Asegurar que tengas todas las migrations
ls services/api/alembic/versions/  # Verificar archivos
```

### Error: Migration falla con "relation already exists"

**Solución:**
```bash
# Opción 1: Marcar como aplicada sin ejecutar
docker compose exec api alembic stamp head

# Opción 2: Reset completo
make db-reset
```

### Adminer no carga

**Solución:**
```bash
# Verificar que Adminer esté corriendo
docker ps | grep adminer

# Verificar logs
docker logs mlp_adminer

# Restart servicios
make dev-restart
```

---

## ✅ Checklist Final

- [ ] Services corriendo (`make dev-up`)
- [ ] Container API rebuildeado con SQLAlchemy (`make build-api`)
- [ ] Primera migration generada (`make db-migrate-create MSG="..."`)
- [ ] Migration revisada (archivo en `alembic/versions/`)
- [ ] Migration aplicada (`make db-migrate`)
- [ ] Seed data cargado (`make db-seed`)
- [ ] DB verificada en Adminer (http://localhost/database)
- [ ] Usuario admin puede hacer login (email: admin@example.com, pass: Admin123!)

---

**¡Listo!** Tu base de datos está configurada y lista para usar. 🎉

**Próximo paso:** Configurar monitoreo de PostgreSQL con Prometheus.

---

**FIN DEL DOCUMENTO**
