# Ruta: /REAL_ESTATE_AGENT/graph/nodes/classifier.py

from typing import Dict, Any
from datetime import datetime
from tools.redis import guardar_en_historial, guardar_contexto
from tools.intent_embeddings import clasificar_por_semantica

class GraphState(dict):
    pass

def clasificar_intencion_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Clasifica la intención del usuario usando un enfoque híbrido por capas,
    dando prioridad máxima a las keywords explícitas.
    """
    print("---🎯 NODO: CLASIFICAR INTENCIÓN (v8 - A Prueba de Balas)---")
    pregunta = state.get("pregunta", "").lower().strip()
    usuario = state.get("usuario", "anonimo")
    intencion = ""

    # --- CAPA 1: Keywords de Acción de Alta Prioridad ---
    # Estas son las acciones más importantes y específicas.
    if any(p in pregunta for p in ["agendar", "visitar", "cita", "turno", "verla"]):
        intencion = "agendar"
        print("✔ Detectado por keyword de MÁXIMA prioridad → agendar")
    
    elif any(p in pregunta for p in ["favorito", "favoritos", "guarda", "guardar", "agregar", "añadir", "quitar", "eliminar", "borrar"]):
        intencion = "favorito"
        print("✔ Detectado por keyword de MÁXIMA prioridad → favorito")

    elif any(p in pregunta for p in ["comparar", "compara", "diferencias", "vs"]):
        intencion = "comparar"
        print("✔ Detectado por keyword de alta prioridad → comparar")

    # --- CAPA 2: Keywords de Búsqueda ---
    # Se comprueba solo si no se encontró una acción de mayor prioridad.
    elif any(p in pregunta for p in ["buscar", "busco", "mostrar", "mostrame", "casa", "casas", "depto", "deptos", "departamento", "alquiler", "venta"]):
        intencion = "buscar"
        print("✔ Detectado por keyword de búsqueda → buscar")

    # --- CAPA 3: Fallback a Semántica ---
    # Solo si NINGUNA keyword coincidió, intentamos con embeddings.
    else:
        intencion_semantica = clasificar_por_semantica(pregunta)
        intencion = intencion_semantica
        print(f"✔ Detectado por embeddings como último recurso → {intencion}")

    # El log final nos dice qué se decidió antes de guardar.
    print(f"==> Intención final decidida: {intencion}")

    guardar_en_historial(usuario, pregunta, intencion, "")
    guardar_contexto(usuario, "ultima_intencion", {"intencion": intencion})
    
    return {"intencion": intencion}