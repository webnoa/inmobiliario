from langchain_core.tools import tool
from tools.db import get_connection
import re

# Lista de ubicaciones soportadas
UBICACIONES = [
    "San Miguel de Tucumán", "Yerba Buena", "Lules", "Tafí Viejo", 
    "Barrio Norte", "Recoleta", "Palermo", "Belgrano"
]

# Sinónimos para tipo de operación
SINONIMOS_VENTA = ["venta", "comprar", "adquirir"]
SINONIMOS_ALQUILER = ["alquiler", "alquilar", "rentar", "arrendar"]

# Sinónimos para tipos de propiedad (no usados aún, pero listos para filtrar por tipo)
SINONIMOS_DEPTO = ["departamento", "depto", "dpto", "piso"]
SINONIMOS_CASA = ["casa", "hogar", "vivienda", "quinta"]
SINONIMOS_MONOAMBIENTE = ["monoambiente", "1 ambiente", "ambiente único"]

@tool
def buscar_propiedades(pregunta: str) -> str:
    """
    Busca propiedades en función de una pregunta en lenguaje natural.
    Aplica filtros básicos como tipo (venta/alquiler), ubicación, precio y ambientes.
    Acepta sinónimos comunes.
    """
    p_lower = pregunta.lower()

    # Detectar tipo de operación
    tipo = None
    for palabra in SINONIMOS_VENTA:
        if palabra in p_lower:
            tipo = "venta"
            break
    for palabra in SINONIMOS_ALQUILER:
        if palabra in p_lower:
            tipo = "alquiler"
            break

    # Detectar ubicación mencionada
    ubicacion = next((loc for loc in UBICACIONES if loc.lower() in p_lower), None)

    # Buscar número de ambientes (ej: "2 amb", "3 ambientes")
    ambientes_match = re.search(r"(\d+)\s*(amb|ambientes)", p_lower)
    ambientes = int(ambientes_match.group(1)) if ambientes_match else None

    # Buscar precio máximo (ej: "hasta 100000", "menos de 90000")
    precio_match = re.search(r"(menos de|hasta)\s*(\d{2,7})", p_lower)
    precio_max = int(precio_match.group(2)) if precio_match else None

    query = "SELECT title, location, price FROM properties WHERE TRUE"
    params = []

    if tipo:
        query += " AND type = %s"
        params.append(tipo)
    if ubicacion:
        query += " AND LOWER(location) = %s"
        params.append(ubicacion.lower())
    if ambientes:
        query += " AND rooms = %s"
        params.append(ambientes)
    if precio_max:
        query += " AND price <= %s"
        params.append(precio_max)

    query += " LIMIT 5"

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, tuple(params))
    rows = cur.fetchall()
    cur.close()
    conn.close()

    if not rows:
        return "No se encontraron propiedades que coincidan con tu búsqueda."

    return "\n".join([f"{r[0]} - {r[1]} - USD {r[2]}" for r in rows])
