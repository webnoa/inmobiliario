from typing import TypedDict
from tools.redis import guardar_en_historial

class GraphState(TypedDict):
    pregunta: str
    intencion: str
    respuesta: str
    usuario: str

def agendar_visita_node(state: GraphState) -> GraphState:
    respuesta = "Simulamos agendamiento de visita. Un asesor se contactará con usted."
    guardar_en_historial(state["usuario"], state["pregunta"], state["intencion"], respuesta)
    return {**state, "respuesta": respuesta}