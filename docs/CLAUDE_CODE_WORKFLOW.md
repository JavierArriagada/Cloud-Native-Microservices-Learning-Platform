# Flujo de Trabajo con Claude Code

**Versión:** 1.0.0
**Fecha:** 2025-12-19
**Propósito:** Documentar el uso de Claude Code, plugins y skills para desarrollo eficiente del proyecto

---

## Tabla de Contenidos

- [1. Introducción](#1-introducción)
- [2. Plugins Instalados](#2-plugins-instalados)
- [3. Skills Disponibles](#3-skills-disponibles)
- [4. Flujo de Trabajo por Fase](#4-flujo-de-trabajo-por-fase)
- [5. Ejemplos Prácticos](#5-ejemplos-prácticos)
- [6. Best Practices](#6-best-practices)
- [7. Troubleshooting](#7-troubleshooting)

---

## 1. Introducción

Claude Code es una CLI interactiva que acelera el desarrollo mediante:
- **Plugins**: Extensiones que añaden capacidades específicas (LSP, Git, GitHub)
- **Skills**: Comandos especializados invocables con `/nombre-skill`
- **Agentes**: Tareas autónomas para exploración, planificación y verificación

Este documento detalla cómo aprovechar estas herramientas en el contexto del proyecto de microservicios.

---

## 2. Plugins Instalados

### 2.1 typescript-lsp (Language Server Protocol)

**Para qué:** Desarrollo del frontend React TypeScript

**Características:**
- Autocompletado inteligente en `.tsx` y `.ts`
- Detección de errores de tipos en tiempo real
- Navegación a definiciones (`Go to Definition`)
- Refactorización segura (renombrado de variables, extracción de componentes)

**Archivos donde actúa:**
```
services/react-app/
├── src/
│   ├── main.tsx
│   ├── App.tsx
│   ├── components/
│   ├── pages/
│   ├── hooks/
│   ├── services/
│   └── types/
```

**Ejemplo de uso:**
```typescript
// Al escribir, el LSP sugiere tipos automáticamente
import { useState } from 'react';

interface User {
  id: number;
  name: string;
  email: string;
}

// Autocompletado de propiedades
const user: User = {
  id: 1,
  name: 'Javier',
  email: // LSP sugiere string
}
```

---

### 2.2 pyright-lsp (Language Server Protocol)

**Para qué:** Desarrollo de API FastAPI y Dash App

**Características:**
- Validación de tipos en Pydantic models
- Autocompletado en routers, schemas y services
- Detección de errores en async/await
- Ayuda con imports y referencias

**Archivos donde actúa:**
```
services/api/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models/      # Pydantic schemas
│   ├── queries/     # SQL queries
│   ├── routers/
│   └── services/

services/dash-app/
├── app/
│   ├── main.py
│   ├── layouts/
│   ├── components/
│   └── callbacks/
```

**Ejemplo de uso:**
```python
# FastAPI - el LSP valida tipos Pydantic
from pydantic import BaseModel

class ItemCreate(BaseModel):
    name: str
    price: float

# Si intentas asignar tipo incorrecto, el LSP lo detecta
item = ItemCreate(
    name="Product",
    price="invalid"  # Error: expected float, got str
)
```

---

### 2.3 commit-commands

**Para qué:** Gestión eficiente de commits y PRs

**Skills disponibles:**
- `/commit` - Crear commit con mensaje bien formado
- `/commit-push-pr` - Commit + push + crear PR automáticamente
- `/clean_gone` - Limpiar branches eliminados en remoto

**Ventajas:**
- Mensajes de commit consistentes
- Automáticamente incluye co-author de Claude
- Detecta cambios y sugiere mensaje apropiado
- Sigue convenciones (feat, fix, docs, refactor)

**Ejemplo de uso:**
```bash
# Scenario: Has modificado services/api/app/main.py

# Opción 1: Solo commit
/commit

# Claude analiza cambios y crea:
# "feat(api): add health check endpoint
#
# - Implement /health endpoint
# - Add database connection validation
#
# 🤖 Generated with Claude Code
# Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"

# Opción 2: Commit + Push + PR
/commit-push-pr

# Claude ejecuta:
# 1. git add .
# 2. git commit -m "..."
# 3. git push -u origin feature-branch
# 4. gh pr create --title "Add health check endpoint" --body "..."
```

---

### 2.4 github

**Para qué:** Interactuar con GitHub sin salir de Claude Code

**Capacidades:**
- Crear y listar PRs
- Ver status de GitHub Actions
- Gestionar issues
- Revisar checks de CI/CD

**Comandos útiles (via Bash):**
```bash
# Ver PRs abiertos
gh pr list

# Ver estado de checks en un PR
gh pr checks 123

# Ver logs de un workflow fallido
gh run view <run-id> --log

# Crear issue
gh issue create --title "Bug: API timeout" --body "..."
```

**Integración con CI/CD:**
```bash
# Monitorear pipeline CI después de push
gh run watch

# Ver errores específicos de un job
gh run view --log-failed
```

---

### 2.5 agent-sdk-dev

**Para qué:** Crear agentes Claude personalizados para tareas específicas

**Skills disponibles:**
- `/new-sdk-app` - Crear nueva aplicación con Agent SDK
- Agentes de verificación para TypeScript y Python

**Posibles agentes personalizados para este proyecto:**

#### Agente 1: SQL Query Validator
```python
# Agente que valida queries SQL antes de ejecutar
# - Detecta SQL injection
# - Verifica sintaxis PostgreSQL
# - Sugiere índices para optimización
```

#### Agente 2: Docker Compose Validator
```python
# Agente que revisa docker-compose.yml
# - Verifica healthchecks
# - Valida redes y volúmenes
# - Detecta configuraciones inseguras
```

#### Agente 3: Kubernetes Manifest Reviewer
```python
# Agente para manifests de K8s
# - Valida recursos y límites
# - Revisa security contexts
# - Verifica configuración de ingress
```

#### Agente 4: Prometheus Metrics Analyzer
```python
# Agente que analiza métricas de Prometheus
# - Detecta anomalías
# - Sugiere alertas
# - Genera reportes de rendimiento
```

**Cómo crear un agente:**
```bash
# 1. Usar skill para crear estructura
/new-sdk-app

# 2. Claude pregunta:
# - Nombre del agente
# - Lenguaje (Python/TypeScript)
# - Propósito

# 3. Claude genera estructura completa
# 4. Implementas lógica específica
# 5. Despliegas y usas desde Claude Code
```

---

## 3. Skills Disponibles

### 3.1 Skills de Git (commit-commands)

| Skill | Descripción | Cuándo usar |
|-------|-------------|-------------|
| `/commit` | Crear commit con mensaje automático | Después de hacer cambios significativos |
| `/commit-push-pr` | Commit + push + crear PR | Completar feature y abrir PR |
| `/clean_gone` | Limpiar branches [gone] | Después de merge de PRs |

**Ejemplo de workflow completo:**
```bash
# 1. Desarrollo
# Implementas feature en services/api/

# 2. Commit
/commit

# 3. Continuar desarrollo o abrir PR
/commit-push-pr  # Si feature está completa

# 4. Limpieza periódica
/clean_gone  # Cada semana
```

---

### 3.2 Skills de Agent SDK

| Skill | Descripción | Cuándo usar |
|-------|-------------|-------------|
| `/new-sdk-app` | Crear app Agent SDK | Crear agente personalizado |

**Casos de uso específicos:**

#### Caso 1: Agente para revisar queries SQL
```bash
# Crear agente
/new-sdk-app

# Configurar:
# - Nombre: sql-query-reviewer
# - Lenguaje: Python
# - Propósito: Validar queries SQL y detectar problemas

# Usar en desarrollo:
"Revisa esta query SQL para vulnerabilidades y optimizaciones:
SELECT * FROM users WHERE id = {user_input}"
```

#### Caso 2: Agente para analizar Docker Compose
```bash
/new-sdk-app

# Configurar:
# - Nombre: docker-compose-validator
# - Propósito: Revisar configuraciones Docker

# Usar antes de commit:
"Valida mi docker-compose.yml antes de hacer commit"
```

---

### 3.3 Skills Integrados de Claude Code

Estos skills están disponibles sin plugins:

| Comando | Descripción |
|---------|-------------|
| `/help` | Ver ayuda de Claude Code |
| `/clear` | Limpiar conversación |
| `/tasks` | Ver tareas en background |

---

## 4. Flujo de Trabajo por Fase

### Fase 1: Estructura Base

**Objetivo:** Crear directorios, Makefile, .env.example

**Workflow:**
```bash
# 1. Pedir a Claude crear estructura
"Crea la estructura base del proyecto según MICROSERVICES_MASTER_PLAN.md"

# 2. Claude crea archivos usando Write tool

# 3. Commit automático
/commit
# Output: "chore: initialize project structure"

# 4. Verificar
make check-deps  # Verificar prerrequisitos
```

**Plugins activos:** commit-commands

---

### Fase 2: Hello World (PostgreSQL + API)

**Objetivo:** Levantar PostgreSQL y API con /health

**Workflow:**

#### 2.1 Desarrollo API FastAPI
```bash
# 1. Crear main.py
"Implementa FastAPI básico con /health endpoint según el plan"

# Mientras escribes, pyright-lsp actúa:
# - Autocompletado de FastAPI imports
# - Validación de tipos Pydantic
# - Detección de errores async/await

# 2. Crear database.py con asyncpg
"Implementa conexión PostgreSQL con asyncpg"

# pyright-lsp ayuda con:
# - Tipos de asyncpg (Connection, Pool)
# - Validación de connection strings

# 3. Crear Dockerfile
"Crea Dockerfile para API FastAPI"

# 4. Commit
/commit
# Output: "feat(api): implement health check endpoint"
```

#### 2.2 Configurar PostgreSQL
```bash
# 1. Docker Compose
"Agrega PostgreSQL al docker-compose.yml con healthcheck"

# 2. Inicializar Alembic
"Inicializa Alembic para migraciones de PostgreSQL"

# pyright-lsp ayuda con:
# - env.py de Alembic
# - Scripts de migración

# 3. Commit
/commit
# Output: "feat(database): setup PostgreSQL with Alembic"
```

#### 2.3 Testing
```bash
# Levantar servicios
make dev-up

# Ver logs
make dev-logs

# Si hay errores, Claude analiza logs y sugiere fixes

# Commit final
/commit-push-pr
# Crea PR "Phase 2: Hello World Complete"
```

**Plugins activos:** pyright-lsp, commit-commands, github

---

### Fase 3: Frontend React

**Objetivo:** Implementar React app con TypeScript

**Workflow:**

```bash
# 1. Crear estructura React
"Crea React app con Vite + TypeScript según estructura del plan"

# 2. Implementar componentes (typescript-lsp activo)
"Crea componente HomePage.tsx"

# Al escribir, typescript-lsp provee:
interface HomePageProps {
  title: string;
  // LSP autocompleta props
}

export const HomePage: React.FC<HomePageProps> = ({ title }) => {
  const [data, setData] = useState<User[]>([]); // LSP infiere tipo User[]
  // ...
}

# 3. Configurar TanStack Query
"Implementa React Query para fetching de /api/v1/items"

# typescript-lsp ayuda con:
# - Tipos de useQuery
# - Tipos de respuesta API

# 4. Tailwind CSS
"Configura Tailwind CSS en el proyecto React"

# 5. Commit por feature
/commit  # Para cada componente mayor

# 6. PR final
/commit-push-pr
# PR: "feat(frontend): implement React app with TypeScript"
```

**Plugins activos:** typescript-lsp, commit-commands

---

### Fase 4: Dash Dashboard

**Objetivo:** Dashboard Python con Plotly

**Workflow:**

```bash
# 1. Estructura Dash
"Crea Dash app según estructura del plan"

# 2. Layouts (pyright-lsp activo)
"Implementa layout principal con Plotly graphs"

# pyright-lsp ayuda con:
import dash
from dash import html, dcc
import plotly.express as px

# Tipos de componentes Dash
# Validación de callbacks

# 3. Callbacks para interactividad
"Implementa callbacks para actualizar gráficos"

# 4. Conectar a API
"Configura conexión a FastAPI desde Dash"

# 5. Commit
/commit-push-pr
```

**Plugins activos:** pyright-lsp, commit-commands

---

### Fase 5: Traefik + Integración

**Objetivo:** API Gateway con routing

**Workflow:**

```bash
# 1. Configurar Traefik
"Configura Traefik en docker-compose con labels para routing"

# 2. Configurar routing rules
# - /api/* → API
# - /dash/* → Dash
# - /* → React

# 3. Testing manual
make dev-up
curl http://localhost/api/health
curl http://localhost/dash/
curl http://localhost/

# 4. Si falla routing, usar agente explorer
# "Explora la configuración de Traefik y explica por qué /api no rutea correctamente"

# 5. Commit
/commit-push-pr
```

---

### Fase 6: Monitoreo (Prometheus + Grafana)

**Objetivo:** Stack de monitoreo completo

**Workflow:**

```bash
# 1. Prometheus config
"Configura Prometheus para scraping de API y Dash"

# 2. Grafana dashboards
"Crea dashboards Grafana para métricas de servicios"

# 3. Loki para logs
"Configura Loki + Promtail para logs centralizados"

# 4. Testing de métricas
# Abrir http://localhost:9090 (Prometheus)
# Abrir http://localhost:3001 (Grafana)

# 5. Opcional: Crear agente para análisis
/new-sdk-app
# Nombre: prometheus-analyzer
# Propósito: Analizar métricas y detectar anomalías

# 6. Commit
/commit-push-pr
```

**Plugins activos:** commit-commands, agent-sdk-dev (opcional)

---

### Fase 7: CI/CD (GitHub Actions)

**Objetivo:** Pipeline automatizado

**Workflow:**

```bash
# 1. Crear workflows
"Crea GitHub Actions workflows según el plan:
- ci.yml: lint, test, build, security
- cd-staging.yml: deploy staging
- cd-production.yml: deploy production"

# 2. Testing local de workflows (opcional)
# Usar act: https://github.com/nektos/act

# 3. Commit workflows
/commit

# 4. Push y monitorear
/commit-push-pr

# 5. Usar github plugin para ver status
# En Claude Code:
"Muéstrame el status del workflow CI"
# Claude ejecuta: gh run list --workflow=ci.yml

# 6. Ver logs si falla
"Muéstrame los logs del último run fallido"
# Claude ejecuta: gh run view --log-failed
```

**Plugins activos:** commit-commands, github

---

### Fase 8: Kubernetes + GCP

**Objetivo:** Deploy a producción

**Workflow:**

```bash
# 1. Crear manifests Kubernetes
"Crea manifests K8s en infrastructure/kubernetes/ para:
- Deployments (api, dash, react)
- Services
- Ingress
- ConfigMaps
- Secrets"

# 2. Opcional: Agente validador
/new-sdk-app
# Nombre: k8s-manifest-validator
# Propósito: Validar manifests antes de deploy

# 3. Configurar Kustomize
"Crea overlays para staging y production"

# 4. Testing local con kind
make k8s-test-local

# 5. Deploy a GCP
make deploy-staging

# 6. Monitorear con github plugin
"Muéstrame el status del deploy a staging"

# 7. Commit
/commit-push-pr
```

**Plugins activos:** commit-commands, github, agent-sdk-dev (opcional)

---

## 5. Ejemplos Prácticos

### 5.1 Ejemplo: Implementar CRUD completo

**Contexto:** Crear endpoints CRUD para recurso "products"

**Paso a paso:**

```bash
# 1. Pedir a Claude implementar backend
"Implementa CRUD completo para productos en FastAPI:
- Pydantic schemas en models/product.py
- SQL queries en queries/product.py (SQL puro, sin ORM)
- Router en routers/product.py
- Tests en tests/test_product.py"

# Claude usa pyright-lsp mientras escribe:

# models/product.py
from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    name: str  # LSP valida tipo
    price: float
    description: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int

# queries/product.py
# SQL puro según el plan
CREATE_PRODUCT = """
    INSERT INTO products (name, price, description)
    VALUES ($1, $2, $3)
    RETURNING id, name, price, description
"""

GET_PRODUCTS = """
    SELECT id, name, price, description
    FROM products
    ORDER BY id
"""

# routers/product.py
from fastapi import APIRouter, Depends
from app.database import get_db_pool
# LSP ayuda con imports

router = APIRouter(prefix="/v1/products", tags=["products"])

@router.post("/", response_model=ProductResponse)
async def create_product(
    product: ProductCreate,  # LSP valida tipo Pydantic
    pool = Depends(get_db_pool)
):
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            CREATE_PRODUCT,
            product.name,
            product.price,
            product.description
        )
        return ProductResponse(**row)

# 2. Implementar frontend
"Crea componente ProductList.tsx con TanStack Query"

# Claude usa typescript-lsp:

# types/product.ts
export interface Product {
  id: number;
  name: string;
  price: number;
  description?: string;
}

# services/productService.ts
import { Product } from '@/types/product';

export const productService = {
  async getAll(): Promise<Product[]> {
    const response = await fetch('/api/v1/products');
    return response.json();  // LSP infiere Product[]
  }
};

# components/ProductList.tsx
import { useQuery } from '@tanstack/react-query';
import { productService } from '@/services/productService';
import { Product } from '@/types/product';

export const ProductList: React.FC = () => {
  const { data, isLoading } = useQuery({
    queryKey: ['products'],
    queryFn: productService.getAll  // LSP valida función
  });

  if (isLoading) return <div>Loading...</div>;

  return (
    <ul>
      {data?.map((product: Product) => (  // LSP autocompleta propiedades
        <li key={product.id}>
          {product.name} - ${product.price}
        </li>
      ))}
    </ul>
  );
};

# 3. Testing
make test

# 4. Commit
/commit
# Output: "feat(products): implement CRUD endpoints and UI"

# 5. Crear PR
/commit-push-pr
# PR automático con descripción generada
```

**Resultado:**
- Backend completo con validación de tipos (pyright-lsp)
- Frontend tipado con autocompletado (typescript-lsp)
- Commit bien formateado (commit-commands)
- PR creado automáticamente (commit-commands + github)

---

### 5.2 Ejemplo: Debugging con Claude + Plugins

**Contexto:** API retorna 500 en producción

**Workflow:**

```bash
# 1. Ver logs en Grafana Loki
"Muéstrame los últimos logs de error de la API"

# Claude usa Bash tool para query Loki:
curl -G http://localhost:3100/loki/api/v1/query_range \
  --data-urlencode 'query={job="api"} |= "ERROR"' \
  --data-urlencode 'limit=50'

# 2. Analizar stack trace
# Claude identifica: "Database connection timeout"

# 3. Revisar código con LSP
"Lee services/api/app/database.py"

# pyright-lsp detecta:
# - Falta timeout en pool connection
# - No hay retry logic

# 4. Fix propuesto por Claude
"Agrega timeout y retry a database.py"

# Claude edita con validación LSP:
async def get_db_pool():
    return await asyncpg.create_pool(
        dsn=DATABASE_URL,
        min_size=5,
        max_size=20,
        timeout=30.0,  # ✅ Agregado
        command_timeout=10.0,  # ✅ Agregado
        max_queries=50000,
        max_inactive_connection_lifetime=300.0
    )

# 5. Test local
make dev-up
make test

# 6. Commit y deploy
/commit-push-pr

# 7. Monitorear deploy con github plugin
gh run watch  # Ver pipeline en tiempo real
```

---

### 5.3 Ejemplo: Crear Agente SQL Validator

**Objetivo:** Agente que valida queries SQL antes de ejecutar

**Implementación:**

```bash
# 1. Crear agente
/new-sdk-app

# Configuración:
# Nombre: sql-query-validator
# Lenguaje: Python
# Propósito: Validar queries SQL para PostgreSQL

# 2. Claude genera estructura:
sql-query-validator/
├── main.py
├── requirements.txt
└── README.md

# 3. Implementar lógica (Claude ayuda con pyright-lsp)

# main.py
import re
from typing import List, Dict
from anthropic import Anthropic

class SQLValidator:
    def __init__(self):
        self.dangerous_patterns = [
            r'DROP\s+TABLE',
            r'TRUNCATE',
            r'DELETE\s+FROM\s+\w+\s*;',  # DELETE sin WHERE
            r'--',  # Comentarios SQL
            r'/\*.*\*/',  # Comentarios bloque
        ]

    def validate(self, query: str) -> Dict[str, any]:
        """Valida query SQL"""
        results = {
            "is_safe": True,
            "warnings": [],
            "suggestions": []
        }

        # Detectar patrones peligrosos
        for pattern in self.dangerous_patterns:
            if re.search(pattern, query, re.IGNORECASE):
                results["is_safe"] = False
                results["warnings"].append(
                    f"Patrón peligroso detectado: {pattern}"
                )

        # Detectar SQL injection
        if re.search(r'["\'].*\+.*["\']', query):
            results["warnings"].append(
                "Posible SQL injection: concatenación de strings"
            )

        # Sugerir parámetros
        if '%s' in query or '{' in query:
            results["suggestions"].append(
                "Usa $1, $2, etc. para parámetros en PostgreSQL"
            )

        return results

# 4. Usar agente en desarrollo
"Valida esta query SQL:
DELETE FROM users WHERE id = {user_input}"

# Agente responde:
# ⚠️ PELIGRO: SQL Injection detectado
# - Concatenación de strings detectada
# - Usar parámetros: DELETE FROM users WHERE id = $1
# - Validar user_input antes de ejecutar

# 5. Integrar en workflow
# Agregar a pre-commit hook o CI/CD
```

---

## 6. Best Practices

### 6.1 Uso de LSP

**DO:**
- ✅ Confiar en el autocompletado del LSP
- ✅ Leer errores de tipo antes de ejecutar
- ✅ Usar "Go to Definition" para explorar código
- ✅ Refactorizar con LSP (renombrar variables)

**DON'T:**
- ❌ Ignorar warnings del LSP
- ❌ Desactivar validación de tipos
- ❌ Usar `any` en TypeScript sin razón
- ❌ Ignorar sugerencias de imports

---

### 6.2 Commits y PRs

**DO:**
- ✅ Usar `/commit` para mensajes consistentes
- ✅ Commitear por feature, no por archivo
- ✅ Usar `/commit-push-pr` cuando feature está completa
- ✅ Limpiar branches con `/clean_gone` regularmente

**DON'T:**
- ❌ Hacer commits manuales (pierdes co-author)
- ❌ PRs gigantes (dividir en features pequeñas)
- ❌ Commits sin contexto ("fix", "update")
- ❌ Push sin tests locales

**Convenciones de commits:**
```
feat(scope): descripción corta

- Detalle 1
- Detalle 2

🤖 Generated with Claude Code
Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

Prefijos:
- `feat`: Nueva funcionalidad
- `fix`: Bug fix
- `docs`: Documentación
- `refactor`: Refactorización sin cambio funcional
- `test`: Tests
- `chore`: Tareas de mantenimiento
- `perf`: Mejoras de rendimiento

Scopes:
- `api`: Backend FastAPI
- `dash`: Dashboard Dash
- `frontend`: React app
- `infra`: Docker, K8s, CI/CD
- `db`: Base de datos, migraciones

---

### 6.3 Uso de Agentes

**Cuándo crear un agente personalizado:**
- ✅ Tarea repetitiva y específica
- ✅ Validación compleja (SQL, manifests)
- ✅ Análisis de métricas o logs
- ✅ Generación de reportes

**Cuándo NO crear un agente:**
- ❌ Tarea única
- ❌ Mejor hecho con script simple
- ❌ Ya existe herramienta (linter)

---

### 6.4 Workflow Git

**Branches:**
```
main (protegida)
├── feature/add-products-crud
├── feature/traefik-routing
├── fix/api-timeout
└── docs/update-readme
```

**Proceso:**
```bash
# 1. Crear feature branch
git checkout -b feature/add-products-crud

# 2. Desarrollo iterativo
# - Implementar
# - Test local
# - /commit (commits pequeños)

# 3. Feature completa
make test
make lint

# 4. PR
/commit-push-pr

# 5. Monitorear CI
gh run watch

# 6. Merge después de review

# 7. Limpieza
git checkout main
git pull
/clean_gone
```

---

### 6.5 Testing Local

**Antes de cada commit:**
```bash
# 1. Lint
make lint

# 2. Tests unitarios
make test

# 3. Tests de integración
make dev-up
make test-integration

# 4. Verificar logs
make dev-logs

# 5. Si todo OK
/commit
```

**Después de cada PR merge:**
```bash
# 1. Pull main
git checkout main
git pull

# 2. Rebuild images
make build

# 3. Verificar todo funciona
make dev-up
make urls  # Verificar endpoints
```

---

## 7. Troubleshooting

### 7.1 LSP no funciona

**Síntomas:**
- No hay autocompletado
- Errores no se muestran
- "Go to Definition" no funciona

**Soluciones:**

```bash
# 1. Verificar que el plugin está activo
# En Claude Code, revisar lista de plugins

# 2. Reiniciar LSP
# Cerrar y abrir Claude Code

# 3. Para TypeScript: verificar tsconfig.json
{
  "compilerOptions": {
    "strict": true,
    "jsx": "react-jsx",
    "module": "ESNext",
    "target": "ESNext"
  }
}

# 4. Para Python: verificar que Pyright encuentra archivos
# Crear pyrightconfig.json si es necesario
{
  "include": ["services/api/app"],
  "exclude": ["**/node_modules", "**/__pycache__"]
}
```

---

### 7.2 Skills no aparecen

**Síntomas:**
- `/commit` no funciona
- Skills no autocompleatan

**Soluciones:**

```bash
# 1. Verificar plugins instalados
# En settings de Claude Code

# 2. Actualizar plugins
# Desde settings

# 3. Si skill específico falla, reportar
# https://github.com/anthropics/claude-code/issues
```

---

### 7.3 Commits fallan

**Síntomas:**
- `/commit` da error
- Pre-commit hooks fallan

**Soluciones:**

```bash
# 1. Ver qué cambios hay
git status

# 2. Ver diff
git diff

# 3. Si hay archivos sin trackear
git add .

# 4. Si pre-commit hook falla
# Ver output del hook
# Corregir errores (lint, tests)
make lint-fix

# 5. Reintentar
/commit
```

---

### 7.4 GitHub Actions fallan

**Síntomas:**
- CI workflow falla
- Tests pasan local pero fallan en CI

**Workflow de debugging:**

```bash
# 1. Ver logs con github plugin
"Muéstrame los logs del último run fallido de CI"

# Claude ejecuta:
gh run view --log-failed

# 2. Identificar job que falló
# Ejemplo: "test-api" job

# 3. Reproducir local con mismo environment
docker run --rm \
  -v $(pwd):/app \
  -w /app \
  python:3.12-slim \
  bash -c "pip install -r requirements-dev.txt && pytest"

# 4. Fix del problema
# - Actualizar dependencias
# - Corregir test
# - Actualizar workflow

# 5. Commit fix
/commit

# 6. Push y verificar
git push

# 7. Monitorear
gh run watch
```

---

### 7.5 Agente personalizado no funciona

**Síntomas:**
- Agente creado con `/new-sdk-app` da error
- No responde como esperado

**Soluciones:**

```bash
# 1. Verificar estructura
ls -la sql-query-validator/

# Debe tener:
# - main.py (o index.ts)
# - requirements.txt (o package.json)
# - README.md

# 2. Verificar dependencias
pip install -r requirements.txt

# 3. Test local
python main.py

# 4. Ver logs
# Agregar prints/logging en main.py

# 5. Consultar documentación
# https://docs.anthropic.com/agent-sdk
```

---

## 8. Recursos Adicionales

### 8.1 Documentación Oficial

- **Claude Code:** https://github.com/anthropics/claude-code
- **Agent SDK:** https://docs.anthropic.com/agent-sdk
- **GitHub CLI:** https://cli.github.com/manual/

### 8.2 Comandos Útiles

```bash
# Ver todos los plugins instalados
# En Claude Code settings

# Ver skills disponibles
/help

# Ver tareas en background
/tasks

# Limpiar conversación
/clear
```

### 8.3 Atajos de Teclado

| Atajo | Acción |
|-------|--------|
| `/` | Mostrar skills disponibles |
| Tab | Autocompletar skill |
| Ctrl+C | Cancelar comando |

---

## 9. Roadmap de Mejoras

### Próximos pasos para optimizar workflow:

#### Q1 2025
- [ ] Crear agente SQL Validator
- [ ] Crear agente Docker Compose Validator
- [ ] Configurar pre-commit hooks con validation

#### Q2 2025
- [ ] Agente Prometheus Metrics Analyzer
- [ ] Agente K8s Manifest Reviewer
- [ ] Integrar agentes en CI/CD pipeline

#### Q3 2025
- [ ] Dashboard de métricas de desarrollo (commits, PRs, CI time)
- [ ] Agente de documentación automática
- [ ] Templates de componentes React con CLI

---

## 10. Changelog

| Versión | Fecha | Cambios |
|---------|-------|---------|
| 1.0.0 | 2025-12-19 | Versión inicial del documento |

---

**FIN DEL DOCUMENTO**
