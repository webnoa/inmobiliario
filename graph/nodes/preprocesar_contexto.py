# Ruta: /REAL_ESTATE_AGENT/graph/nodes/preprocesar_contexto.py

import re
# --- CAMBIO CLAVE: Añadimos 'Dict' a la importación ---
from typing import TypedDict, Any, Dict

# Importamos la función de Redis
from tools.redis import recuperar_contexto

# Definición del estado del grafo
class GraphState(TypedDict, total=False):
    pregunta: str
    intencion: str
    respuesta: str
    usuario: str
    propiedades_encontradas: list
    datos_visita: dict
    datos_visita_confirmada: dict

# Frases que, si se usan solas, se consideran ambiguas
_FRASES_AMBIGUAS = {
    "y el precio", "cuánto sale", "y la otra", "y las fotos",
    "contame más", "dame más detalles",
    "cual me conviene", "cuál me conviene", "cual me conviene más", "comparala", "compáralas",
    "quiero verla", "agendar una visita", "me interesa"
}

def _es_ambigua(txt: str) -> bool:
    """
    Determina si una pregunta es ambigua basándose en una lista de frases
    o en una heurística simple.
    """
    t = txt.strip().lower()
    if t in _FRASES_AMBIGUAS:
        return True
    # Heurística: menos de 5 palabras y no contiene verbos/sustantivos clave
    if len(t.split()) <= 4 and not re.search(r"(casa|depto|visita|agendar|precio|cuanto|buscar)", t):
        return True
    return False

def preprocesar_contexto_node(state: GraphState) -> Dict[str, Any]:
    """
    Nodo que revisa si la pregunta es ambigua. Si lo es, intenta reemplazarla
    con el contexto de la última pregunta guardada en Redis.
    """
    print("---🧠 NODO: PREPROCESAR CONTEXTO---")
    pregunta = state.get("pregunta", "")
    usuario = state.get("usuario", "anonimo")

    if _es_ambigua(pregunta):
        print(f"Pregunta ambigua detectada: '{pregunta}'")
        
        ultima_pregunta_contexto = recuperar_contexto(usuario, "ultima_pregunta")

        texto_contexto = None
        if isinstance(ultima_pregunta_contexto, dict):
            texto_contexto = ultima_pregunta_contexto.get("texto")
        elif isinstance(ultima_pregunta_contexto, str):
            texto_contexto = ultima_pregunta_contexto
        
        if texto_contexto and texto_contexto != pregunta:
            nueva_pregunta = f"{texto_contexto} y {pregunta}"
            print(f"↩️ Sustituyendo por contexto. Nueva pregunta: '{nueva_pregunta}'")
            return {"pregunta": nueva_pregunta}

    return {}