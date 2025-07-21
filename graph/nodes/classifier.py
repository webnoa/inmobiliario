# Ruta: /REAL_ESTATE_AGENT/graph/nodes/classifier.py

from typing import Dict, Any
from datetime import datetime
from tools.redis import guardar_en_historial, guardar_contexto
from tools.intent_embeddings import clasificar_por_semantica

# ... (la definición de GraphState no cambia) ...
class GraphState(dict): # Usar dict simple es más flexible
    pass

def clasificar_intencion_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Clasifica la intención del usuario con un orden de prioridad lógico y definitivo.
    """
    print("---🎯 NODO: CLASIFICAR INTENCIÓN (v3)---")
    pregunta = state.get("pregunta", "").lower()
    usuario = state.get("usuario", "anonimo")
    intencion = ""

    # --- REGLAS DE CLASIFICACIÓN POR PRIORIDAD DEFINITIVA ---

    # Prioridad 1: Agendar. Es la acción más específica.
    if any(p in pregunta for p in ["agendar", "visitar", "cita", "turno", "verla"]):
        intencion = "agendar"
        print("✔ Detectado por keyword de MÁXIMA prioridad → agendar")

    # Prioridad 2: Comparar.
    elif any(p in pregunta for p in ["comparar", "compara", "diferencias", "vs"]):
        intencion = "comparar"
        print("✔ Detectado por keyword de alta prioridad → comparar")

    # Prioridad 3: Búsqueda.
    elif any(p in pregunta for p in ["buscar", "busco", "mostrar", "mostrame", "casa", "casas", "depto", "deptos", "departamento"]):
        intencion = "buscar"
        print("✔ Detectado por keyword de búsqueda → buscar")

    # Prioridad 4: Fallback a clasificación semántica.
    else:
        intencion = clasificar_por_semantica(pregunta)
        print(f"✔ Detectado por embeddings → {intencion}")

    guardar_en_historial(usuario, pregunta, intencion, "")
    guardar_contexto(usuario, "ultima_intencion", {"intencion": intencion})
    
    return {"intencion": intencion}