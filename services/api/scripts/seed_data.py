"""
Seed Data Script

Script para poblar la base de datos con datos iniciales:
- Roles del sistema (ADMIN, USER, MODERATOR, GUEST)
- Usuario administrador por defecto

Ejecutar con:
    docker compose exec api python -m scripts.seed_data

O desde Makefile:
    make db-seed
"""

import asyncio
import asyncpg
from passlib.context import CryptContext
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.config import settings

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def seed_roles(conn: asyncpg.Connection):
    """Crear roles del sistema"""
    print("📝 Creando roles del sistema...")

    roles = [
        ("ADMIN", "Administrador con acceso completo al sistema", 1000, True),
        ("MODERATOR", "Moderador de contenido y usuarios", 500, True),
        ("USER", "Usuario estándar con acceso básico", 100, True),
        ("GUEST", "Usuario invitado con acceso de solo lectura", 10, True),
    ]

    query = """
        INSERT INTO roles (name, description, priority, is_system)
        VALUES ($1, $2, $3, $4)
        ON CONFLICT (name) DO NOTHING
        RETURNING name
    """

    created_count = 0
    for name, description, priority, is_system in roles:
        result = await conn.fetchrow(query, name, description, priority, is_system)
        if result:
            print(f"  ✅ Rol creado: {name} (prioridad: {priority})")
            created_count += 1
        else:
            print(f"  ℹ️  Rol ya existe: {name}")

    if created_count > 0:
        print(f"✅ {created_count} roles creados")
    else:
        print("ℹ️  Todos los roles ya existían")


async def seed_admin_user(conn: asyncpg.Connection):
    """Crear usuario administrador por defecto"""
    print("\n👤 Creando usuario administrador por defecto...")

    # Default admin credentials (CAMBIAR EN PRODUCCIÓN!)
    admin_email = "admin@example.com"
    admin_username = "admin"
    admin_password = "Admin123!"  # Password temporal

    # Hash password
    password_hash = pwd_context.hash(admin_password)

    # Check if admin already exists
    check_query = """
        SELECT id FROM users
        WHERE email = $1 AND deleted_at IS NULL
    """
    existing_admin = await conn.fetchrow(check_query, admin_email)

    if existing_admin:
        print(f"  ℹ️  Usuario admin ya existe: {admin_email}")
        admin_id = existing_admin["id"]
    else:
        # Create admin user
        create_query = """
            INSERT INTO users (
                email,
                username,
                password_hash,
                first_name,
                last_name,
                is_active,
                is_verified,
                email_verified_at
            )
            VALUES ($1, $2, $3, $4, $5, $6, $7, NOW())
            RETURNING id, email, username
        """

        admin = await conn.fetchrow(
            create_query,
            admin_email,
            admin_username,
            password_hash,
            "System",
            "Administrator",
            True,
            True,
        )
        admin_id = admin["id"]
        print(f"  ✅ Usuario admin creado: {admin['email']}")
        print(f"     Username: {admin['username']}")
        print(f"     Password: {admin_password} (¡CAMBIAR EN PRODUCCIÓN!)")

    # Assign ADMIN role
    print("\n🔑 Asignando rol ADMIN...")

    # Get ADMIN role ID
    role_query = "SELECT id FROM roles WHERE name = 'ADMIN'"
    admin_role = await conn.fetchrow(role_query)

    if not admin_role:
        print("  ❌ Rol ADMIN no encontrado. Ejecuta seed_roles primero.")
        return

    # Assign role
    assign_query = """
        INSERT INTO user_roles (user_id, role_id)
        VALUES ($1, $2)
        ON CONFLICT (user_id, role_id) DO NOTHING
        RETURNING id
    """

    result = await conn.fetchrow(assign_query, admin_id, admin_role["id"])
    if result:
        print("  ✅ Rol ADMIN asignado al usuario administrador")
    else:
        print("  ℹ️  Usuario ya tenía el rol ADMIN")


async def seed_sample_users(conn: asyncpg.Connection):
    """Crear usuarios de ejemplo (opcional)"""
    print("\n👥 Creando usuarios de ejemplo...")

    sample_users = [
        ("user1@example.com", "user1", "User123!", "John", "Doe", "USER"),
        ("user2@example.com", "user2", "User123!", "Jane", "Smith", "USER"),
        ("moderator@example.com", "moderator", "Mod123!", "Mike", "Johnson", "MODERATOR"),
    ]

    created_count = 0
    for email, username, password, first_name, last_name, role_name in sample_users:
        # Check if user exists
        check_query = "SELECT id FROM users WHERE email = $1 AND deleted_at IS NULL"
        existing = await conn.fetchrow(check_query, email)

        if existing:
            print(f"  ℹ️  Usuario ya existe: {email}")
            user_id = existing["id"]
        else:
            # Create user
            password_hash = pwd_context.hash(password)
            create_query = """
                INSERT INTO users (
                    email,
                    username,
                    password_hash,
                    first_name,
                    last_name,
                    is_active,
                    is_verified,
                    email_verified_at
                )
                VALUES ($1, $2, $3, $4, $5, TRUE, TRUE, NOW())
                RETURNING id
            """
            user = await conn.fetchrow(
                create_query,
                email,
                username,
                password_hash,
                first_name,
                last_name,
            )
            user_id = user["id"]
            print(f"  ✅ Usuario creado: {email}")
            created_count += 1

        # Assign role
        role_query = "SELECT id FROM roles WHERE name = $1"
        role = await conn.fetchrow(role_query, role_name)

        if role:
            assign_query = """
                INSERT INTO user_roles (user_id, role_id)
                VALUES ($1, $2)
                ON CONFLICT DO NOTHING
            """
            await conn.execute(assign_query, user_id, role["id"])

    if created_count > 0:
        print(f"✅ {created_count} usuarios de ejemplo creados")


async def seed_audit_logs(conn: asyncpg.Connection):
    """Crear audit logs de ejemplo para testing"""
    print("\n📝 Creando audit logs de ejemplo...")

    # Obtener admin user ID
    admin_query = "SELECT id FROM users WHERE email = 'admin@example.com' LIMIT 1"
    admin = await conn.fetchrow(admin_query)

    if not admin:
        print("  ⚠️  Usuario admin no encontrado. Ejecuta seed_admin_user primero.")
        return

    admin_id = admin["id"]

    # Audit logs de ejemplo
    audit_logs = [
        # Login exitoso
        (
            admin_id,
            "LOGIN",
            None,
            None,
            "Admin user logged in successfully",
            {"browser": "Chrome", "os": "Linux"},
            "127.0.0.1",
            "Mozilla/5.0 (X11; Linux x86_64) Chrome/120.0.0.0"
        ),
        # Creación de usuario
        (
            admin_id,
            "CREATE",
            "users",
            None,  # Would be actual user_id in real scenario
            "Created new user account",
            {"username": "test_user", "email": "test@example.com"},
            "127.0.0.1",
            "Mozilla/5.0 (X11; Linux x86_64) Chrome/120.0.0.0"
        ),
        # Cambio de configuración
        (
            admin_id,
            "CONFIG_CHANGE",
            "system",
            None,
            "Updated system settings",
            {"setting": "max_upload_size", "old_value": "10MB", "new_value": "20MB"},
            "127.0.0.1",
            "Mozilla/5.0 (X11; Linux x86_64) Chrome/120.0.0.0"
        ),
        # Error del sistema (sin user_id)
        (
            None,
            "ERROR",
            "system",
            None,
            "Database connection timeout",
            {"error_code": "DB_TIMEOUT", "duration_ms": 5000},
            None,
            None
        ),
        # Warning del sistema
        (
            None,
            "WARNING",
            "system",
            None,
            "High memory usage detected",
            {"memory_usage_percent": 85, "threshold": 80},
            None,
            None
        ),
        # Login fallido
        (
            None,
            "LOGIN_FAILED",
            None,
            None,
            "Failed login attempt for user: admin@example.com",
            {"reason": "invalid_password", "attempts": 3},
            "192.168.1.100",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Firefox/120.0"
        ),
        # Update de usuario
        (
            admin_id,
            "UPDATE",
            "users",
            None,
            "Updated user profile information",
            {"fields_updated": ["first_name", "last_name"], "username": "admin"},
            "127.0.0.1",
            "Mozilla/5.0 (X11; Linux x86_64) Chrome/120.0.0.0"
        ),
        # Info del sistema
        (
            None,
            "INFO",
            "system",
            None,
            "Database backup completed successfully",
            {"backup_size_mb": 250, "duration_seconds": 45},
            None,
            None
        ),
    ]

    import json
    created_count = 0

    for user_id, action, entity_type, entity_id, description, extra_data, ip, user_agent in audit_logs:
        # Check if similar audit log exists (para no duplicar en re-runs)
        check_query = """
            SELECT id FROM audit_logs
            WHERE action = $1 AND description = $2
            LIMIT 1
        """
        existing = await conn.fetchrow(check_query, action, description)

        if existing:
            continue

        # Create audit log
        import uuid as uuid_lib
        create_query = """
            INSERT INTO audit_logs (
                id,
                user_id,
                action,
                entity_type,
                entity_id,
                description,
                extra_data,
                ip_address,
                user_agent
            )
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
            RETURNING id, action, description
        """

        log = await conn.fetchrow(
            create_query,
            uuid_lib.uuid4(),
            user_id,
            action,
            entity_type,
            entity_id,
            description,
            json.dumps(extra_data) if extra_data else None,
            ip,
            user_agent
        )
        print(f"  ✅ Audit log creado: {log['action']} - {log['description'][:50]}...")
        created_count += 1

    if created_count > 0:
        print(f"✅ {created_count} audit logs creados")
    else:
        print("ℹ️  Todos los audit logs ya existían")


async def main():
    """Main function"""
    print("=" * 70)
    print("  🌱 SEED DATA - Cloud Native Microservices Learning Platform")
    print("=" * 70)
    print()

    # Connect to database
    try:
        print("📡 Conectando a base de datos...")
        conn = await asyncpg.connect(settings.get_db_url_asyncpg())
        print("✅ Conexión establecida")
        print()

        # Seed data
        await seed_roles(conn)
        await seed_admin_user(conn)

        # Uncomment to create sample users
        # await seed_sample_users(conn)

        # Seed audit logs (para testing)
        await seed_audit_logs(conn)

        print()
        print("=" * 70)
        print("  ✅ Seed data completado exitosamente")
        print("=" * 70)
        print()
        print("Credenciales de administrador:")
        print("  Email:    admin@example.com")
        print("  Password: Admin123!")
        print()
        print("⚠️  IMPORTANTE: Cambiar password en producción!")
        print()

    except Exception as e:
        print(f"\n❌ Error: {e}")
        raise
    finally:
        if conn:
            await conn.close()
            print("📡 Conexión cerrada")


if __name__ == "__main__":
    asyncio.run(main())
