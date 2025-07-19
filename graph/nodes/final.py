from typing import TypedDict

class GraphState(TypedDict):
    pregunta: str
    intencion: str
    respuesta: str

def final_node(state: GraphState) -> GraphState:
    return {"respuesta": state.get("respuesta", "No se pudo procesar tu consulta.")}
