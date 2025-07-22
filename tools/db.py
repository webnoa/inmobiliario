# Ruta: /REAL_ESTATE_AGENT/tools/db.py

import psycopg2
import csv
from config import POSTGRES # Asegúrate de que este import funcione y traiga los datos de conexión

# --- Funciones de Conexión y Configuración ---

def get_connection():
    """
    Crea y devuelve una conexión a la base de datos PostgreSQL.
    """
    try:
        connection = psycopg2.connect(
            host=POSTGRES.get("host"),
            port=POSTGRES.get("port"),
            user=POSTGRES.get("user"),
            password=POSTGRES.get("password"),
            dbname=POSTGRES.get("db")
        )
        return connection
    except psycopg2.OperationalError as e:
        print(f"Error al conectar con la base de datos: {e}")
        raise

def create_properties_table():
    """
    Crea la tabla 'properties' en la base de datos si no existe.
    """
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

def load_properties_from_csv(csv_path):
    """
    Carga propiedades desde un archivo CSV a la base de datos.
    Si una propiedad con el mismo ID ya existe, la ignora.
    """
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

# --- Funciones de Búsqueda y Obtención de Datos ---

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

    def normalizar_termino(termino):
        return termino[:-1] if termino.endswith('s') else termino

    terminos_brutos = texto_busqueda.lower().split()
    terminos_filtrados = [
        normalizar_termino(term) for term in terminos_brutos
        if len(term) > 2 and term not in STOP_WORDS
    ]
    
    if not terminos_filtrados:
        return []

    conn = get_connection()
    cur = conn.cursor()
    
    base_query = "SELECT id, title, type, price, location, rooms, area_m2 FROM properties WHERE "
    condiciones = [
        "(LOWER(title) LIKE %s OR LOWER(location) LIKE %s OR LOWER(type) LIKE %s)"
        for _ in terminos_filtrados
    ]
    params = []
    for term in terminos_filtrados:
        params.extend([f"%{term}%", f"%{term}%", f"%{term}%"])

    query = base_query + " AND ".join(condiciones)
    cur.execute(query, tuple(params))
    
    columnas = [desc[0] for desc in cur.description]
    propiedades_encontradas = [dict(zip(columnas, row)) for row in cur.fetchall()]
    
    cur.close()
    conn.close()
    return propiedades_encontradas

def obtener_propiedades_por_ids(ids: list) -> list:
    """
    Obtiene una lista de propiedades de la base de datos según una lista de IDs.
    Asegura que los IDs se traten como enteros para evitar errores de tipo en SQL.
    """
    if not ids:
        return []
        
    conn = get_connection()
    cur = conn.cursor()
    
    # --- CORRECCIÓN CLAVE: Asegurarse de que los IDs son enteros ---
    # Convertimos todos los elementos de la lista a int antes de la consulta.
    try:
        ids_enteros = [int(i) for i in ids]
    except (ValueError, TypeError):
        # Si la lista contiene algo que no es un número, devolvemos una lista vacía.
        return []
    
    # Ahora pasamos la lista de enteros a la consulta.
    query = "SELECT id, title, type, price, location, rooms, area_m2 FROM properties WHERE id = ANY(%s)"
    cur.execute(query, (ids_enteros,))
    
    columnas = [desc[0] for desc in cur.description]
    propiedades_encontradas = [dict(zip(columnas, row)) for row in cur.fetchall()]
    
    cur.close()
    conn.close()
    
    return propiedades_encontradas