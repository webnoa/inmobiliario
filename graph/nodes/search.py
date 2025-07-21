# Ruta: /REAL_ESTATE_AGENT/graph/nodes/search.py

from typing import Dict, Any
from tools.db import buscar_propiedades_por_texto

def buscar_propiedades_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Nodo que utiliza la función de búsqueda de tools/db.py para encontrar
    propiedades y luego formatea una respuesta para el usuario.
    """
    print("---🔎 NODO: BUSCAR PROPIEDADES (usando tools.db)---")
    pregunta = state.get("pregunta", "")

    try:
        propiedades_encontradas = buscar_propiedades_por_texto(pregunta)
    except Exception as e:
        print(f"Error al llamar a buscar_propiedades_por_texto: {e}")
        return {"respuesta": "Lo siento, tuve un problema al realizar la búsqueda."}

    if propiedades_encontradas:
        respuesta_texto = "¡Claro! Consultando la base de datos, encontré estas propiedades:\n\n"
        for prop in propiedades_encontradas:
            precio = prop.get('price', 0)
            tipo_operacion = prop.get('type', 'N/A').capitalize()
            
            respuesta_texto += (
                f"**ID {prop.get('id')}**: {prop.get('title', 'Sin título')}\n"
                f"  - **Tipo**: {tipo_operacion}\n"
                f"  - **Ubicación**: {prop.get('location', 'N/A')}\n"
                f"  - **Precio**: ${precio:,}\n"
                f"  - **Ambientes**: {prop.get('rooms', 'N/A')}\n"
                f"  - **Superficie**: {prop.get('area_m2', 'N/A')} m²\n\n"
            )
        respuesta_texto += "Puedes pedirme que las compare usando sus IDs o agendar una visita."
    else:
        respuesta_texto = "Lo siento, no encontré propiedades en la base de datos que coincidan con tu búsqueda."

    return {
        "propiedades_encontradas": propiedades_encontradas,
        "respuesta": respuesta_texto
    }