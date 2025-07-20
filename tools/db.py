import psycopg2
import csv
from config import POSTGRES

# Crea una conexión a PostgreSQL
def get_connection():
    return psycopg2.connect(
        host=POSTGRES["host"],
        port=POSTGRES["port"],
        user=POSTGRES["user"],
        password=POSTGRES["password"],
        dbname=POSTGRES["db"]
    )

# Crea la tabla de propiedades si no existe
def create_properties_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS properties (
            id SERIAL PRIMARY KEY,
            title TEXT,
            type TEXT,
            price INTEGER,
            location TEXT,
            rooms INTEGER,
            area_m2 INTEGER
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

# Carga propiedades desde un archivo CSV
def load_properties_from_csv(csv_path):
    conn = get_connection()
    cur = conn.cursor()

    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cur.execute("""
                INSERT INTO properties (title, type, price, location, rooms, area_m2)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                row["title"],
                row["type"],
                int(row["price"]),
                row["location"],
                int(row["rooms"]),
                int(row["area_m2"])
            ))

    conn.commit()
    cur.close()
    conn.close()

# Dummy para evitar crash - buscar por texto
def buscar_propiedades(texto_busqueda: str):
    return [
        {"id": 1, "tipo": "Casa", "ambientes": 3, "ubicacion": "San Miguel", "precio": 75000},
        {"id": 2, "tipo": "Departamento", "ambientes": 2, "ubicacion": "Yerba Buena", "precio": 58000},
    ]

# Dummy para evitar crash - buscar por IDs
def obtener_propiedades_por_ids(ids):
    dummy = [
        {"id": 1, "tipo": "Casa", "ambientes": 3, "ubicacion": "San Miguel", "precio": 75000},
        {"id": 2, "tipo": "Departamento", "ambientes": 2, "ubicacion": "Yerba Buena", "precio": 58000},
        {"id": 3, "tipo": "Casa", "ambientes": 4, "ubicacion": "Tafí Viejo", "precio": 95000},
    ]
    return [p for p in dummy if p["id"] in ids]
