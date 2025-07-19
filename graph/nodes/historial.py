# graph/nodes/historial.py

from typing import TypedDict

class GraphState(TypedDict):
    pregunta: str
    intencion: str
    respuesta: str
    usuario: str

def guardar_historial_node(state: GraphState) -> GraphState:
    # Nodo "passthrough" temporal — solo retorna el estado sin cambios
    return state
