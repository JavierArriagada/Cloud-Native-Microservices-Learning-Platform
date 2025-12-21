# Code Generation & Seed Data Workflow

Documentación completa del sistema de generación automática de código y datos de seed para la plataforma.

## Tabla de Contenidos

1. [Arquitectura General](#arquitectura-general)
2. [Scripts Disponibles](#scripts-disponibles)
3. [Flujo de Trabajo Completo](#flujo-de-trabajo-completo)
4. [generate_model.py](#generate_modelpy)
5. [generate_code.py](#generate_codepy)
6. [seed_data.py](#seed_datapy)
7. [seed_mining_data.py](#seed_mining_datapy)
8. [create_table.sh](#create_tablesh)
9. [Ejemplos de Uso](#ejemplos-de-uso)

---

## Arquitectura General

```mermaid
flowchart TB
    subgraph Database["PostgreSQL Database"]
        DB[(Base de Datos)]
        Tables[Tablas Existentes]
    end

    subgraph Scripts["Scripts de Generación"]
        GM[generate_model.py]
        GC[generate_code.py]
        CT[create_table.sh]
    end

    subgraph SeedScripts["Scripts de Seed"]
        SD[seed_data.py]
        SMD[seed_mining_data.py]
    end

    subgraph GeneratedCode["Código Generado"]
        DBM[db_models/*.py<br/>SQLAlchemy Models]
        PYD[models/*.py<br/>Pydantic Schemas]
        SQL[queries/*.py<br/>SQL Queries]
    end

    subgraph Alembic["Migraciones"]
        ALB[alembic/versions/*.py]
    end

    DB --> GM
    GM --> DBM
    DBM --> GC
    GC --> PYD
    GC --> SQL
    DBM --> ALB
    ALB --> DB

    SD --> DB
    SMD --> DB

    CT --> GM
    CT --> GC
    CT --> ALB

    style Database fill:#336699,color:#fff
    style Scripts fill:#66aa66,color:#fff
    style SeedScripts fill:#aa6666,color:#fff
    style GeneratedCode fill:#996633,color:#fff
    style Alembic fill:#663399,color:#fff
```

---

## Scripts Disponibles

| Script | Propósito | Entrada | Salida |
|--------|-----------|---------|--------|
| `generate_model.py` | Generar modelo SQLAlchemy desde DB existente | Nombre de tabla | `db_models/{tabla}.py` |
| `generate_code.py` | Generar Pydantic schemas y queries SQL | Nombre de modelo | `models/{tabla}.py`, `queries/{tabla}.py` |
| `seed_data.py` | Poblar datos base (roles, admin, etc.) | - | Datos en DB |
| `seed_mining_data.py` | Poblar datos del dominio minero | - | Datos en DB |
| `create_table.sh` | Workflow interactivo completo | Interactivo | Todo lo anterior |

---

## Flujo de Trabajo Completo

```mermaid
sequenceDiagram
    autonumber
    participant Dev as Desarrollador
    participant CT as create_table.sh
    participant GM as generate_model.py
    participant ALB as Alembic
    participant GC as generate_code.py
    participant DB as PostgreSQL
    participant SD as seed_data.py

    Dev->>CT: Ejecutar script interactivo
    CT->>Dev: Solicitar nombre de tabla
    Dev->>CT: Proporcionar información

    CT->>GM: Crear template de modelo
    GM-->>CT: db_models/{tabla}.py

    Dev->>Dev: Editar columnas del modelo

    CT->>ALB: Generar migración
    ALB-->>CT: versions/{migration}.py

    Dev->>Dev: Revisar migración

    CT->>ALB: Aplicar migración
    ALB->>DB: CREATE TABLE
    DB-->>ALB: OK

    CT->>GC: Generar código
    GC-->>CT: models/{tabla}.py
    GC-->>CT: queries/{tabla}.py

    Dev->>Dev: Actualizar __init__.py

    opt Seed Data
        CT->>SD: Ejecutar seed
        SD->>DB: INSERT datos
    end

    CT->>Dev: Workflow completado
```

---

## generate_model.py

### Descripción

Genera un modelo SQLAlchemy automáticamente desde una tabla existente en la base de datos usando `sqlacodegen`.

### Diagrama de Flujo

```mermaid
flowchart TD
    A[Inicio] --> B{Argumentos válidos?}
    B -->|No| C[Mostrar uso]
    C --> Z[Fin]

    B -->|Sí| D[Conectar a PostgreSQL]
    D --> E[Ejecutar sqlacodegen]
    E --> F{Generación exitosa?}

    F -->|No| G[Mostrar error]
    G --> Z

    F -->|Sí| H[Crear archivo db_models/tabla.py]
    H --> I[Agregar docstring]
    I --> J[Guardar archivo]
    J --> K[Mostrar pasos siguientes]
    K --> Z

    style A fill:#4CAF50,color:#fff
    style Z fill:#f44336,color:#fff
    style H fill:#2196F3,color:#fff
```

### Uso

```bash
# Desde el contenedor Docker
docker compose exec api python -m scripts.generate_model products

# Directamente (requiere conexión DB)
python scripts/generate_model.py products
```

### Salida Generada

```python
"""
Products SQLAlchemy Model

Generado automáticamente desde la base de datos.
"""

from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
# ... modelo generado por sqlacodegen
```

---

## generate_code.py

### Descripción

Genera automáticamente:
1. **Pydantic Schemas**: Para validación de requests/responses
2. **SQL Queries**: Operaciones CRUD con asyncpg

### Diagrama de Arquitectura

```mermaid
flowchart LR
    subgraph Input["Entrada"]
        Model[SQLAlchemy Model<br/>db_models/*.py]
    end

    subgraph Process["Procesamiento"]
        Load[Cargar Modelo]
        Analyze[Analizar Columnas]
        MapTypes[Mapear Tipos SQL → Python]
    end

    subgraph Output["Salida"]
        PydanticBase["{Model}Base"]
        PydanticCreate["{Model}Create"]
        PydanticUpdate["{Model}Update"]
        PydanticInDB["{Model}InDB"]
        PydanticPublic["{Model}Public"]

        QueryGet["get_{model}_by_id()"]
        QueryGetAll["get_all_{model}s()"]
        QueryCreate["create_{model}()"]
        QueryUpdate["update_{model}()"]
        QueryDelete["delete_{model}()"]
    end

    Model --> Load
    Load --> Analyze
    Analyze --> MapTypes

    MapTypes --> PydanticBase
    PydanticBase --> PydanticCreate
    PydanticBase --> PydanticUpdate
    PydanticBase --> PydanticInDB
    PydanticBase --> PydanticPublic

    MapTypes --> QueryGet
    MapTypes --> QueryGetAll
    MapTypes --> QueryCreate
    MapTypes --> QueryUpdate
    MapTypes --> QueryDelete

    style Input fill:#E3F2FD,stroke:#1976D2
    style Process fill:#FFF3E0,stroke:#F57C00
    style Output fill:#E8F5E9,stroke:#388E3C
```

### Mapeo de Tipos

```mermaid
flowchart LR
    subgraph SQL["Tipos SQL"]
        UUID_SQL[UUID]
        VARCHAR[VARCHAR]
        TEXT[TEXT]
        INTEGER[INTEGER]
        NUMERIC[NUMERIC]
        BOOLEAN[BOOLEAN]
        TIMESTAMP[TIMESTAMP]
        DATE[DATE]
    end

    subgraph Python["Tipos Python"]
        UUID_PY[UUID]
        STR[str]
        INT[int]
        DECIMAL[Decimal]
        BOOL[bool]
        DATETIME[datetime]
        DATE_PY[date]
    end

    UUID_SQL --> UUID_PY
    VARCHAR --> STR
    TEXT --> STR
    INTEGER --> INT
    NUMERIC --> DECIMAL
    BOOLEAN --> BOOL
    TIMESTAMP --> DATETIME
    DATE --> DATE_PY
```

### Uso

```bash
# Generar código para el modelo 'product'
docker compose exec api python -m scripts.generate_code product
```

### Estructura de Schemas Generados

```mermaid
classDiagram
    class ProductBase {
        +name: str
        +description: Optional[str]
        +price: Decimal
        +category_id: Optional[UUID]
    }

    class ProductCreate {
        <<Request - POST>>
    }

    class ProductUpdate {
        +name: Optional[str]
        +description: Optional[str]
        +price: Optional[Decimal]
        +category_id: Optional[UUID]
    }

    class ProductInDB {
        +id: UUID
        +created_at: datetime
        +updated_at: datetime
        +model_config: from_attributes
    }

    class ProductPublic {
        <<Response - API>>
        +id: UUID
        +created_at: datetime
        +model_config: from_attributes
    }

    ProductBase <|-- ProductCreate
    ProductBase <|-- ProductInDB
    ProductBase <|-- ProductPublic
    BaseModel <|-- ProductUpdate
```

---

## seed_data.py

### Descripción

Pobla la base de datos con datos iniciales esenciales:
- Roles del sistema (ADMIN, MODERATOR, USER, GUEST)
- Usuario administrador por defecto
- Logs de auditoría de ejemplo

### Diagrama de Ejecución

```mermaid
flowchart TD
    A[Inicio seed_data.py] --> B[Conectar a PostgreSQL]
    B --> C{Conexión OK?}

    C -->|No| Z1[Error: Conexión fallida]
    C -->|Sí| D[seed_roles]

    subgraph Roles["seed_roles()"]
        D --> D1[ADMIN - prioridad 1000]
        D1 --> D2[MODERATOR - prioridad 500]
        D2 --> D3[USER - prioridad 100]
        D3 --> D4[GUEST - prioridad 10]
    end

    D4 --> E[seed_admin_user]

    subgraph Admin["seed_admin_user()"]
        E --> E1[Verificar si existe admin]
        E1 --> E2{Existe?}
        E2 -->|Sí| E3[Usar existente]
        E2 -->|No| E4[Crear usuario admin]
        E3 --> E5[Asignar rol ADMIN]
        E4 --> E5
    end

    E5 --> F[seed_audit_logs]

    subgraph Audit["seed_audit_logs()"]
        F --> F1[LOGIN exitoso]
        F1 --> F2[CREATE usuario]
        F2 --> F3[CONFIG_CHANGE]
        F3 --> F4[ERROR sistema]
        F4 --> F5[LOGIN_FAILED]
    end

    F5 --> G[Cerrar conexión]
    G --> H[Mostrar credenciales]
    H --> Z2[Fin exitoso]

    style A fill:#4CAF50,color:#fff
    style Z1 fill:#f44336,color:#fff
    style Z2 fill:#4CAF50,color:#fff
```

### Datos Creados

```mermaid
erDiagram
    ROLES ||--o{ USER_ROLES : has
    USERS ||--o{ USER_ROLES : has
    USERS ||--o{ AUDIT_LOGS : creates

    ROLES {
        uuid id PK
        string name "ADMIN, MODERATOR, USER, GUEST"
        string description
        int priority "1000, 500, 100, 10"
        bool is_system
    }

    USERS {
        uuid id PK
        string email "admin@example.com"
        string username "admin"
        string password_hash "bcrypt"
        bool is_active
        bool is_verified
    }

    AUDIT_LOGS {
        uuid id PK
        uuid user_id FK
        string action "LOGIN, CREATE, UPDATE..."
        string entity_type
        json extra_data
    }
```

### Uso

```bash
# Ejecutar seed básico
docker compose exec api python -m scripts.seed_data

# Desde Makefile
make db-seed
```

---

## seed_mining_data.py

### Descripción

Pobla la base de datos con datos realistas del dominio minero chileno, incluyendo entidades maestras de Capa 1.

### Jerarquía de Entidades

```mermaid
flowchart TB
    subgraph Layer1["Capa 1: Entidades Maestras"]
        DEP[Deposits<br/>Yacimientos]
        MIN[Mines<br/>Minas]
        PHA[Mine Phases<br/>Fases]
        BLK[Blocks<br/>Modelo de Bloques]

        EQT[Equipment Types<br/>Tipos de Equipo]
        EQ[Equipment<br/>Equipos]
        OP[Operators<br/>Operadores]

        REA[Reagents<br/>Reactivos]
        PA[Process Areas<br/>Áreas de Proceso]

        CRD[Coordinates<br/>Coordenadas]
        MNL[Mineralogy<br/>Mineralogía]
    end

    DEP --> MIN
    DEP --> CRD
    DEP --> MNL
    MIN --> PHA
    PHA --> BLK
    MIN --> EQ
    EQT --> EQ
    MIN --> OP
    MIN --> PA

    style DEP fill:#4CAF50,color:#fff
    style MIN fill:#2196F3,color:#fff
    style PHA fill:#9C27B0,color:#fff
```

### Orden de Ejecución (Respeta Foreign Keys)

```mermaid
sequenceDiagram
    autonumber
    participant Script as seed_mining_data.py
    participant DB as PostgreSQL

    Note over Script,DB: Entidades sin dependencias
    Script->>DB: seed_deposits() - El Teniente, Chuquicamata, Escondida
    Script->>DB: seed_equipment_types() - Camiones, Palas, Molinos...
    Script->>DB: seed_reagents() - PAX, MIBC, Cal...

    Note over Script,DB: Entidades con FK a deposits
    Script->>DB: seed_coordinates() - Lat/Long/UTM
    Script->>DB: seed_mineralogy() - Calcopirita, Bornita...
    Script->>DB: seed_mines() - Minas por yacimiento

    Note over Script,DB: Entidades con FK a mines
    Script->>DB: seed_mine_phases() - 3 fases por mina
    Script->>DB: seed_equipment() - Equipos por mina
    Script->>DB: seed_operators() - Personal por mina
    Script->>DB: seed_process_areas() - Chancado, Molienda, Flotación...

    Note over Script,DB: Entidades con FK a phases
    Script->>DB: seed_blocks() - 75 bloques de muestra
```

### Datos de Ejemplo (Minería Chilena)

```mermaid
mindmap
  root((Datos Mineros))
    Yacimientos
      El Teniente
        Pórfido Cuprífero
        O'Higgins
        4500 Mt Recursos
      Chuquicamata
        Antofagasta
        Mayor rajo abierto
      Escondida
        Mayor productor Cu
        BHP
    Equipos
      Mina
        CAT 797F - Camión 400t
        CAT 7495 - Pala 75m³
        Atlas Copco D75KS
      Planta
        Chancador Metso
        Molino SAG FLSmidth
        Celdas Outotec
    Reactivos
      Colectores
        PAX - Xantato
        SIPX
        Aerophine 3418A
      Espumantes
        MIBC
        Dowfroth 250
      Depresantes
        NaHS
        CMC
    Mineralogía
      Mena
        Calcopirita CuFeS2
        Bornita Cu5FeS4
        Molibdenita MoS2
      Ganga
        Pirita FeS2
        Cuarzo SiO2
```

### Uso

```bash
# Ejecutar seed de datos mineros
docker compose exec api python -m scripts.seed_mining_data

# Desde Makefile
make db-seed-mining
```

---

## create_table.sh

### Descripción

Script interactivo que orquesta todo el workflow de creación de una nueva tabla, desde la definición hasta la verificación.

### Flujo Interactivo

```mermaid
stateDiagram-v2
    [*] --> Recopilar: Ejecutar script

    Recopilar --> CrearModelo: Nombre, descripción
    state CrearModelo {
        [*] --> Template
        Template --> Edición: Usuario edita columnas
        Edición --> [*]
    }

    CrearModelo --> ActualizarInit: Modelo listo
    ActualizarInit --> GenerarMigración

    state GenerarMigración {
        [*] --> Autogenerate
        Autogenerate --> Revisar: Migración generada
        Revisar --> Confirmar
        Confirmar --> [*]
    }

    GenerarMigración --> AplicarMigración
    AplicarMigración --> GenerarCódigo

    state GenerarCódigo {
        [*] --> Schemas: Pydantic
        Schemas --> Queries: SQL
        Queries --> [*]
    }

    GenerarCódigo --> Verificar

    state Verificar {
        [*] --> VerificarDB: \\d tabla
        VerificarDB --> [*]
    }

    Verificar --> SeedData: Opcional
    SeedData --> [*]: Completado
    Verificar --> [*]: Sin seed
```

### Archivos Generados

```mermaid
flowchart LR
    subgraph Input["Entrada"]
        USER[Usuario]
    end

    subgraph Script["create_table.sh"]
        direction TB
        S1[1. Recopilar info]
        S2[2. Crear modelo]
        S3[3. Actualizar __init__]
        S4[4. Generar migración]
        S5[5. Aplicar migración]
        S6[6. Generar código]
        S7[7. Verificar DB]
    end

    subgraph Output["Archivos Generados"]
        F1[db_models/tabla.py]
        F2[db_models/__init__.py]
        F3[alembic/versions/xxx.py]
        F4[models/tabla.py]
        F5[queries/tabla.py]
    end

    USER --> S1
    S1 --> S2
    S2 --> F1
    S2 --> S3
    S3 --> F2
    S3 --> S4
    S4 --> F3
    S4 --> S5
    S5 --> S6
    S6 --> F4
    S6 --> F5
    S6 --> S7

    style Input fill:#E3F2FD
    style Script fill:#FFF3E0
    style Output fill:#E8F5E9
```

### Uso

```bash
# Ejecutar workflow interactivo
./services/api/scripts/create_table.sh

# Pasos del script:
# 1. Nombre de tabla: product
# 2. Nombre plural: products
# 3. Descripción: Productos del catálogo
# 4. Mensaje migración: add products table
```

---

## Ejemplos de Uso

### Crear Nueva Tabla Completa

```mermaid
sequenceDiagram
    participant Dev as Desarrollador
    participant Shell as Terminal
    participant Docker as Docker Compose
    participant DB as PostgreSQL

    Dev->>Shell: ./scripts/create_table.sh
    Shell->>Dev: Nombre de tabla?
    Dev->>Shell: category
    Shell->>Dev: Nombre plural?
    Dev->>Shell: categories

    Shell->>Shell: Crear template db_models/category.py
    Dev->>Dev: Editar modelo (agregar columnas)

    Shell->>Docker: alembic revision --autogenerate
    Docker-->>Shell: Migración creada

    Shell->>Docker: alembic upgrade head
    Docker->>DB: CREATE TABLE categories

    Shell->>Docker: python -m scripts.generate_code category
    Docker-->>Shell: models/category.py
    Docker-->>Shell: queries/category.py

    Shell->>Docker: psql -c "\\d categories"
    Docker->>DB: Describe table
    DB-->>Dev: Estructura de tabla
```

### Poblar Base de Datos Completa

```bash
# 1. Seed datos base (roles, admin)
make db-seed

# 2. Seed datos mineros
make db-seed-mining

# 3. Verificar datos
docker compose exec postgres psql -U mlp_user -d mlp_db -c "
  SELECT 'roles' as tabla, count(*) FROM roles
  UNION ALL
  SELECT 'users', count(*) FROM users
  UNION ALL
  SELECT 'deposits', count(*) FROM deposits
  UNION ALL
  SELECT 'mines', count(*) FROM mines
  UNION ALL
  SELECT 'equipment', count(*) FROM equipment;
"
```

---

## Resumen de Comandos

```mermaid
flowchart TB
    subgraph Makefile["Comandos Make"]
        M1[make db-seed]
        M2[make db-seed-mining]
        M3[make db-migrate]
    end

    subgraph Docker["Comandos Docker"]
        D1[docker compose exec api<br/>python -m scripts.generate_model tabla]
        D2[docker compose exec api<br/>python -m scripts.generate_code tabla]
        D3[docker compose exec api<br/>python -m scripts.seed_data]
        D4[docker compose exec api<br/>python -m scripts.seed_mining_data]
    end

    subgraph Shell["Scripts Shell"]
        S1[./scripts/create_table.sh]
    end

    M1 --> D3
    M2 --> D4
    S1 --> D1
    S1 --> D2
```

---

## Diagrama de Dependencias de Archivos

```mermaid
flowchart TB
    subgraph Config["Configuración"]
        CFG[app/config.py<br/>settings.get_db_url_asyncpg]
    end

    subgraph DBModels["db_models/"]
        INIT[__init__.py<br/>Base, modelos]
        USERS[users.py]
        ROLES[roles.py]
        DEPOSITS[deposits.py]
    end

    subgraph Scripts["scripts/"]
        GM[generate_model.py]
        GC[generate_code.py]
        SD[seed_data.py]
        SMD[seed_mining_data.py]
        CT[create_table.sh]
    end

    subgraph Output["Código Generado"]
        MODELS[models/*.py]
        QUERIES[queries/*.py]
    end

    CFG --> SD
    CFG --> SMD
    CFG --> GM

    INIT --> GC
    GC --> MODELS
    GC --> QUERIES

    CT --> GM
    CT --> GC

    SD --> INIT
    SMD --> INIT
```
