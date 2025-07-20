
"""Nodo previo al react_agent: completa/sustituye la pregunta con contexto si es ambigua o vacía."""
import re
from typing import TypedDict
from tools.redis import recuperar_contexto

class GraphState(TypedDict, total=False):
    pregunta: str
    intencion: str
    respuesta: str
    usuario: str

_FRASES_AMBIGUAS = {
    "", "seguí", "y?", "y eso", "dale", "ok", "contame más", "mostrame", "¿y ahora?",
    "cual me conviene", "cuál me conviene", "cual me conviene más", "comparala",
}

def _es_ambigua(txt: str) -> bool:
    t = txt.strip().lower()
    if t in _FRASES_AMBIGUAS:
        return True
    # heurística: menos de 5 palabras y no contiene verbos claros
    if len(t.split()) <= 4 and not re.search(r"(casa|depto|visita|agendar|precio|cuanto|buscar)", t):
        return True
    return False

def preprocesar_contexto_node(state: GraphState) -> GraphState:
    pregunta = state.get("pregunta", "")
    usuario = state.get("usuario", "anonimo")

    if _es_ambigua(pregunta):
        ultima = recuperar_contexto(usuario, "ultima_pregunta") or {}
        nueva = ultima.get("texto") or pregunta
        if nueva != pregunta:
            print(f"↩️ Pregunta ambigua, sustituyo por último contexto: {nueva}")
            return {**state, "pregunta": nueva}
    return state
