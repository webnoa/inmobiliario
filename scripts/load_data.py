# Script para crear tabla y cargar propiedades desde CSV
from tools.db import create_properties_table, load_properties_from_csv

if __name__ == "__main__":
    create_properties_table()
    load_properties_from_csv("data/properties.csv")
    print("✅ Datos cargados con éxito")
