#!/usr/bin/env python3
"""
Generar Modelo SQLAlchemy desde Base de Datos Existente

Este script usa sqlacodegen para inspeccionar la DB y generar
el modelo SQLAlchemy automáticamente.
"""

import subprocess
import sys
from pathlib import Path

def generate_sqlalchemy_model(table_name: str):
    """Generar modelo SQLAlchemy usando sqlacodegen"""

    # Comando para generar el modelo
    cmd = [
        "sqlacodegen",
        "--generator", "declarative",
        "--tables", table_name,
        f"postgresql://user:password@localhost:5432/dbname"  # TODO: usar variables de entorno
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error generando modelo: {e}")
        print(f"Stderr: {e.stderr}")
        return None

def main():
    if len(sys.argv) < 2:
        print("Uso: python generate_model.py <table_name>")
        print("Ejemplo: python generate_model.py products")
        sys.exit(1)

    table_name = sys.argv[1]

    print(f"Generando modelo SQLAlchemy para tabla '{table_name}'...")

    # Generar código
    code = generate_sqlalchemy_model(table_name)

    if code:
        # Guardar en archivo
        output_file = Path(__file__).parent / "app" / "db_models" / f"{table_name}.py"

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f'"""\n{table_name.title()} SQLAlchemy Model\n\nGenerado automáticamente desde la base de datos.\n"""\n\n')
            f.write(code)

        print(f"✅ Modelo generado: {output_file}")
        print("\n📝 Pasos siguientes:")
        print("1. Revisar y ajustar el modelo generado")
        print("2. Importar en db_models/__init__.py")
        print("3. Ejecutar: python scripts/generate_code.py {table_name}")
    else:
        print("❌ Error generando el modelo")
        sys.exit(1)

if __name__ == "__main__":
    main()