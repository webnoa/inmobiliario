from typing import TypedDict
from tools.redis import guardar_en_historial, guardar_contexto

class GraphState(TypedDict):
    pregunta: str
    intencion: str
    respuesta: str
    usuario: str

def guardar_historial_node(state: GraphState) -> GraphState:
    usuario = state["usuario"]
    pregunta = state["pregunta"]
    intencion = state["intencion"]
    respuesta = state["respuesta"]

    # Guardar historial completo
    guardar_en_historial(usuario, pregunta, intencion, respuesta)

    # Guardar en contexto actual
    guardar_contexto(usuario, "ultima_intencion", intencion)
    guardar_contexto(usuario, "ultima_pregunta", pregunta)
    guardar_contexto(usuario, "ultima_respuesta", respuesta)

    return state