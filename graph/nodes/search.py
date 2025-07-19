from typing import TypedDict
from tools.property_search import buscar_propiedades
from tools.redis import guardar_en_historial

class GraphState(TypedDict):
    pregunta: str
    intencion: str
    respuesta: str
    usuario: str

def buscar_propiedades_node(state: GraphState) -> GraphState:
    respuesta = buscar_propiedades(state["pregunta"])
    guardar_en_historial(state["usuario"], state["pregunta"], state["intencion"], respuesta)
    return {**state, "respuesta": respuesta}