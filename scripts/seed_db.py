# Ruta: /REAL_ESTATE_AGENT/scripts/seed_db.py

import sys
import os

# Añadir la raíz del proyecto al path para que podamos importar 'tools'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tools.db import create_properties_table, load_properties_from_csv

def main():
    """
    Script para inicializar la base de datos: crea la tabla y carga los datos.
    """
    print("Iniciando la inicialización de la base de datos...")
    
    try:
        # 1. Crear la tabla si no existe
        print("Creando la tabla 'properties' (si no existe)...")
        create_properties_table()
        print("Tabla 'properties' verificada/creada con éxito.")
        
        # 2. Cargar los datos desde el CSV
        # Asegúrate de que la ruta al CSV sea correcta desde la raíz del proyecto
        csv_path = 'data/properties.csv' 
        print(f"Cargando datos desde '{csv_path}'...")
        load_properties_from_csv(csv_path)
        print("¡Datos cargados con éxito en la base de datos!")
        
    except Exception as e:
        print(f"Ocurrió un error durante la inicialización: {e}")

if __name__ == "__main__":
    main()