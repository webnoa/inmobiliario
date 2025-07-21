# Ruta: /REAL_ESTATE_AGENT/tools/db.py

import psycopg2
import csv
from config import POSTGRES

# --- Funciones de Conexión y Configuración (sin cambios) ---
def get_connection():
    return psycopg2.connect(
        host=POSTGRES.get("host"), port=POSTGRES.get("port"),
        user=POSTGRES.get("user"), password=POSTGRES.get("password"),
        dbname=POSTGRES.get("db")
    )

def create_properties_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS properties (
            id SERIAL PRIMARY KEY, title TEXT, type TEXT, price INTEGER,
            location TEXT, rooms INTEGER, area_m2 INTEGER
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

def load_properties_from_csv(csv_path):
    conn = get_connection()
    cur = conn.cursor()
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cur.execute("""
                INSERT INTO properties (id, title, type, price, location, rooms, area_m2)
                VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (id) DO NOTHING
            """, (
                int(row["id"]), row["title"], row["type"], int(row["price"]),
                row["location"], int(row["rooms"]), int(row["area_m2"])
            ))
    conn.commit()
    cur.close()
    conn.close()

# En /REAL_ESTATE_AGENT/tools/db.py

# En /REAL_ESTATE_AGENT/tools/db.py

# En /REAL_ESTATE_AGENT/tools/db.py

def buscar_propiedades_por_texto(texto_busqueda: str) -> list:
    """
    Busca propiedades en la DB. Normaliza términos (plural a singular)
    y filtra "stop words" para una búsqueda precisa con AND.
    """
    STOP_WORDS = {
        "busco", "buscar", "quiero", "comprar", "alquilar", "necesito",
        "mostrar", "mostrame", "dame", "ver",
        "en", "de", "un", "una", "el", "la", "los", "las", "con"
    }

    # --- CAMBIO CLAVE: Normalización de términos ---
    def normalizar_termino(termino):
        # Reglas simples de singularización
        if termino.endswith('s'):
            return termino[:-1]
        return termino

    terminos_brutos = texto_busqueda.lower().split()
    terminos_filtrados = [
        normalizar_termino(term) for term in terminos_brutos
        if len(term) > 2 and term not in STOP_WORDS
    ]
    
    print(f"\n---[DEBUG DB] Términos de búsqueda extraídos (filtrados y normalizados): {terminos_filtrados}\n")

    if not terminos_filtrados:
        return []

    conn = get_connection()
    cur = conn.cursor()
    
    base_query = "SELECT id, title, type, price, location, rooms, area_m2 FROM properties WHERE "
    
    condiciones = []
    params = []
    for term in terminos_filtrados:
        # Usamos el término normalizado para la búsqueda
        condiciones.append("(LOWER(title) LIKE %s OR LOWER(location) LIKE %s OR LOWER(type) LIKE %s)")
        params.extend([f"%{term}%", f"%{term}%", f"%{term}%"])

    query = base_query + " AND ".join(condiciones)
    
    print(f"---[DEBUG DB] Consulta a ejecutar:\n{cur.mogrify(query, tuple(params)).decode('utf-8')}\n")
    
    cur.execute(query, tuple(params))
    
    columnas = [desc[0] for desc in cur.description]
    propiedades_encontradas = [dict(zip(columnas, row)) for row in cur.fetchall()]
    
    print(f"---[DEBUG DB] Filas encontradas: {len(propiedades_encontradas)}\n")
    
    cur.close()
    conn.close()
    
    return propiedades_encontradas

# --- Función de Obtención por IDs (sin cambios) ---
def obtener_propiedades_por_ids(ids: list) -> list:
    if not ids: return []
    conn = get_connection()
    cur = conn.cursor()
    query = "SELECT id, title, type, price, location, rooms, area_m2 FROM properties WHERE id = ANY(%s)"
    cur.execute(query, (ids,))
    columnas = [desc[0] for desc in cur.description]
    propiedades_encontradas = [dict(zip(columnas, row)) for row in cur.fetchall()]
    cur.close()
    conn.close()
    return propiedades_encontradas