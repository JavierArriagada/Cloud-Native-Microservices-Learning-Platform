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
