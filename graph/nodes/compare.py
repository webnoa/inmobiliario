# Ruta: /REAL_ESTATE_AGENT/graph/nodes/compare.py

import re
from typing import Dict, Any
# Importamos la función para buscar por IDs desde nuestra herramienta de DB
from tools.db import obtener_propiedades_por_ids

def comparar_propiedades_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Compara propiedades. Primero busca en el contexto y, si no las encuentra,
    las busca directamente en la base de datos usando sus IDs.
    """
    print("---⚖️ NODO: COMPARAR PROPIEDADES (INTELIGENTE)---")
    pregunta = state.get("pregunta", "")
    
    # Extraer todos los IDs numéricos de la pregunta
    ids_a_comparar = [int(id_str) for id_str in re.findall(r'\d+', pregunta)]

    if len(ids_a_comparar) < 2:
        return {"respuesta": "Por favor, dime los IDs de al menos dos propiedades que quieres comparar (ej: 'compara la 1 y la 5')."}

    # --- NUEVA LÓGICA INTELIGENTE ---
    propiedades_en_contexto = state.get("propiedades_encontradas", [])
    propiedades_filtradas = [prop for prop in propiedades_en_contexto if prop["id"] in ids_a_comparar]

    # Comprobar si encontramos todas las propiedades necesarias en el contexto
    if len(propiedades_filtradas) < len(ids_a_comparar):
        print(f"No se encontraron todos los IDs en el contexto. Buscando en la DB...")
        try:
            # Si faltan, vamos a la base de datos a buscarlas todas
            propiedades_filtradas = obtener_propiedades_por_ids(ids_a_comparar)
        except Exception as e:
            print(f"Error al buscar propiedades por ID en la DB: {e}")
            return {"respuesta": "Tuve un problema al buscar los detalles de esas propiedades en la base de datos."}

    if len(propiedades_filtradas) < 2:
        return {"respuesta": "No pude encontrar al menos dos de las propiedades con los IDs que mencionaste. ¿Estás seguro de que los IDs son correctos?"}

    # Tomamos las dos primeras propiedades encontradas para la comparación
    prop1, prop2 = propiedades_filtradas[0], propiedades_filtradas[1]
    respuesta_texto = f"Aquí tienes una comparación entre la propiedad **ID {prop1['id']}** y la **ID {prop2['id']}**:\n\n"
    
    if prop1.get('price', 0) < prop2.get('price', 0):
        respuesta_texto += f"💰 **Precio**: La opción {prop1['id']} (${prop1.get('price', 0):,}) es más económica.\n"
    else:
        respuesta_texto += f"💰 **Precio**: La opción {prop2['id']} (${prop2.get('price', 0):,}) es más económica.\n"

    if prop1.get('rooms', 0) > prop2.get('rooms', 0):
        respuesta_texto += f"🛏️ **Ambientes**: La opción {prop1['id']} tiene más ambientes ({prop1.get('rooms', 0)}).\n"
    elif prop2.get('rooms', 0) > prop1.get('rooms', 0):
        respuesta_texto += f"🛏️ **Ambientes**: La opción {prop2['id']} tiene más ambientes ({prop2.get('rooms', 0)}).\n"
    else:
        respuesta_texto += f"🛏️ **Ambientes**: Ambas tienen la misma cantidad de ambientes ({prop1.get('rooms', 0)}).\n"

    respuesta_texto += "\n¿Te gustaría agendar una visita para alguna de ellas?"

    return {"respuesta": respuesta_texto}