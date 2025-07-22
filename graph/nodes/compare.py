# Ruta: /REAL_ESTATE_AGENT/graph/nodes/compare.py

import re
from typing import Dict, Any
# Importamos la función para buscar por IDs desde nuestra herramienta de DB
from tools.db import obtener_propiedades_por_ids

def comparar_propiedades_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Compara propiedades. Es robusto y maneja errores inesperados.
    1. Extrae IDs de la pregunta.
    2. Busca los IDs en el contexto de la conversación actual.
    3. Si faltan, los busca directamente en la base de datos.
    4. Genera una comparación en texto o un mensaje de error amigable.
    """
    print("---⚖️ NODO: COMPARAR PROPIEDADES (INTELIGENTE Y ROBUSTO)---")
    
    try:
        pregunta = state.get("pregunta", "")
        
        # Extraer todos los IDs numéricos de la pregunta
        ids_a_comparar = [int(id_str) for id_str in re.findall(r'\d+', pregunta)]

        if len(ids_a_comparar) < 2:
            return {"respuesta": "Por favor, dime los IDs de al menos dos propiedades que quieres comparar (ej: 'compara la 1 y la 5')."}

        # --- Lógica Inteligente de Búsqueda ---
        propiedades_en_contexto = state.get("propiedades_encontradas", [])
        propiedades_filtradas = [prop for prop in propiedades_en_contexto if prop.get("id") in ids_a_comparar]

        # Comprobar si encontramos todas las propiedades necesarias en el contexto
        if len(propiedades_filtradas) < len(ids_a_comparar):
            print(f"No se encontraron todos los IDs en el contexto. Buscando en la DB...")
            # Si faltan, vamos a la base de datos a buscarlas todas
            propiedades_filtradas = obtener_propiedades_por_ids(ids_a_comparar)

        if len(propiedades_filtradas) < 2:
            return {"respuesta": "No pude encontrar al menos dos de las propiedades con los IDs que mencionaste. ¿Estás seguro de que los IDs son correctos?"}

        # Tomamos las dos primeras propiedades encontradas para la comparación
        prop1, prop2 = propiedades_filtradas[0], propiedades_filtradas[1]
        respuesta_texto = f"Aquí tienes una comparación entre la propiedad **ID {prop1.get('id')}** y la **ID {prop2.get('id')}**:\n\n"
        
        # Comparación de precio
        if prop1.get('price', 0) < prop2.get('price', 0):
            respuesta_texto += f"💰 **Precio**: La opción {prop1.get('id')} (${prop1.get('price', 0):,}) es más económica.\n"
        else:
            respuesta_texto += f"💰 **Precio**: La opción {prop2.get('id')} (${prop2.get('price', 0):,}) es más económica.\n"

        # Comparación de ambientes
        if prop1.get('rooms', 0) > prop2.get('rooms', 0):
            respuesta_texto += f"🛏️ **Ambientes**: La opción {prop1.get('id')} tiene más ambientes ({prop1.get('rooms', 0)}).\n"
        elif prop2.get('rooms', 0) > prop1.get('rooms', 0):
            respuesta_texto += f"🛏️ **Ambientes**: La opción {prop2.get('id')} tiene más ambientes ({prop2.get('rooms', 0)}).\n"
        else:
            respuesta_texto += f"🛏️ **Ambientes**: Ambas tienen la misma cantidad de ambientes ({prop1.get('rooms', 0)}).\n"
        
        # Comparación de superficie
        if prop1.get('area_m2', 0) > prop2.get('area_m2', 0):
            respuesta_texto += f"📏 **Superficie**: La opción {prop1.get('id')} es más grande ({prop1.get('area_m2', 0)} m²).\n"
        elif prop2.get('area_m2', 0) > prop1.get('area_m2', 0):
            respuesta_texto += f"📏 **Superficie**: La opción {prop2.get('id')} es más grande ({prop2.get('area_m2', 0)} m²).\n"
        
        respuesta_texto += "\n¿Te gustaría agendar una visita para alguna de ellas?"

        return {"respuesta": respuesta_texto}

    except Exception as e:
        # --- CAPTURA DE ERRORES INESPERADOS ---
        # Si algo falla (ej: un dato malformado, un error de conexión que no se capturó en tools/db.py),
        # este bloque evitará que el agente se rompa.
        print(f"🚨 ERROR INESPERADO en comparar_propiedades_node: {e}")
        return {"respuesta": "¡Ups! Ocurrió un error inesperado al intentar comparar las propiedades. Por favor, inténtalo de nuevo."}