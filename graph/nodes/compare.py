from typing import TypedDict
from tools.redis import guardar_en_historial

class GraphState(TypedDict):
    pregunta: str
    intencion: str
    respuesta: str
    usuario: str

def comparar_propiedades_node(state: GraphState) -> GraphState:
    respuesta = (
        "Comparación de propiedades:\n"
        "- Propiedad A: Casa en Yerba Buena, 3 amb, USD 75.000\n"
        "- Propiedad B: Depto en SM Tucumán, 2 amb, USD 65.000\n"
        "→ La propiedad A tiene más espacio pero es más cara.\n"
    )
    guardar_en_historial(state["usuario"], state["pregunta"], state["intencion"], respuesta)
    return {**state, "respuesta": respuesta}