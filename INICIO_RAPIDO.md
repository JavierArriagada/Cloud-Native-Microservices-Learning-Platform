# ⚡ Inicio Rápido - 5 Minutos

> Instala y ejecuta la plataforma completa en menos de 5 minutos.

---

## 🎯 Opción 1: Script de Instalación (Más Rápido)

```bash
# 1. Clonar y entrar al proyecto
git clone https://github.com/JavierArriagada/Cloud-Native-Microservices-Learning-Platform.git
cd Cloud-Native-Microservices-Learning-Platform

# 2. Ejecutar instalación automatizada
./install.sh
```

**¡Eso es todo!** El script se encarga de:
- ✅ Verificar requisitos (Docker, Git)
- ✅ Configurar variables de entorno
- ✅ Construir imágenes
- ✅ Levantar servicios
- ✅ Aplicar migraciones
- ✅ Cargar datos de ejemplo

---

## 🛠️ Opción 2: Instalación con Makefile

```bash
# 1. Clonar el proyecto
git clone https://github.com/JavierArriagada/Cloud-Native-Microservices-Learning-Platform.git
cd Cloud-Native-Microservices-Learning-Platform

# 2. Instalación completa en un comando
make -f Makefile.install install
```

**Comandos útiles del Makefile:**
```bash
make -f Makefile.install check-requirements  # Verificar requisitos
make -f Makefile.install install-quick       # Instalación rápida
make -f Makefile.install install-full        # Instalación completa
make -f Makefile.install verify              # Verificar servicios
make -f Makefile.install help                # Ver todos los comandos
```

---

## 🔧 Opción 3: Instalación Manual

```bash
# 1. Clonar el proyecto
git clone https://github.com/JavierArriagada/Cloud-Native-Microservices-Learning-Platform.git
cd Cloud-Native-Microservices-Learning-Platform

# 2. Configurar entorno
cp .env.example .env

# 3. Levantar servicios
docker compose -f infrastructure/docker/docker-compose.yml \
               -f infrastructure/docker/docker-compose.dev.yml \
               up -d

# 4. Aplicar migraciones
docker exec -it mlp-api-1 python -m alembic upgrade head

# 5. Cargar datos de ejemplo (opcional)
docker exec -it mlp-api-1 python -m scripts.seed_data
```

---

## 🌐 Acceder a los Servicios

Una vez instalado, abre tu navegador en:

| Servicio | URL | Descripción |
|----------|-----|-------------|
| 🌐 **Frontend** | http://localhost | Aplicación web principal |
| 📚 **API Docs** | http://localhost/api/docs | Documentación interactiva |
| 📊 **Dashboard** | http://localhost/dash | Panel de métricas |
| 🔀 **Traefik** | http://localhost:8080 | Gateway |
| 📈 **Grafana** | http://localhost:3001 | Monitoreo (admin/admin_change_in_production) |

---

## 🛑 Detener los Servicios

```bash
# Detener todos los servicios
docker compose -f infrastructure/docker/docker-compose.yml \
               -f infrastructure/docker/docker-compose.dev.yml \
               down
```

---

## 📚 Siguiente Paso

Para instrucciones detalladas y solución de problemas, consulta:

- **[Guía de Instalación Completa](docs/GUIA_INSTALACION.md)** - Instalación paso a paso
- **[README Principal](README.md)** - Descripción general del proyecto
- **[Documentación](docs/README.md)** - Toda la documentación disponible

---

## 🆘 Problemas Comunes

### Puerto en uso
```bash
# Ver qué está usando el puerto 80
sudo lsof -i :80

# O cambiar puerto en .env
echo "TRAEFIK_HTTP_PORT=8080" >> .env
```

### Docker no está corriendo
```bash
# Linux
sudo systemctl start docker

# macOS/Windows: Abre Docker Desktop
```

### PostgreSQL no responde
```bash
# Esperar a que esté listo
docker exec mlp-postgres-1 pg_isready -U mlp_user

# Reiniciar si es necesario
docker restart mlp-postgres-1
```

---

## 📋 Requisitos Mínimos

- **Docker Desktop** 20.10+ (con Docker Compose v2)
- **Git** 2.30+
- **4 GB RAM** disponible para contenedores
- **5 GB** de espacio en disco

---

**¿Necesitas ayuda?** Abre un issue en GitHub o consulta la [documentación completa](docs/GUIA_INSTALACION.md).
