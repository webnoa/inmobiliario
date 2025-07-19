from typing import TypedDict
from langgraph.graph import StateGraph
from graph.nodes.classifier import clasificar_intencion
from graph.nodes.search import buscar_propiedades_node
from graph.nodes.compare import comparar_propiedades_node
from graph.nodes.agenda import agendar_visita_node
from graph.nodes.react_agent import react_agent_node
from graph.nodes.historial import guardar_historial_node  # ✅ NUEVO

class GraphState(TypedDict):
    pregunta: str
    intencion: str
    respuesta: str
    usuario: str

def build_graph():
    builder = StateGraph(GraphState)

    # Nodos principales
    builder.add_node("clasificar_intencion", clasificar_intencion)
    builder.add_node("buscar_propiedades", buscar_propiedades_node)
    builder.add_node("comparar_propiedades", comparar_propiedades_node)
    builder.add_node("agendar_visita", agendar_visita_node)
    builder.add_node("react_agent", react_agent_node)
    builder.add_node("guardar_historial", guardar_historial_node)  # ✅ nuevo nodo

    # Punto de entrada
    builder.set_entry_point("clasificar_intencion")

    # Transiciones por intención
    builder.add_conditional_edges(
        "clasificar_intencion",
        lambda state: state["intencion"],
        {
            "buscar": "buscar_propiedades",
            "comparar": "comparar_propiedades",
            "agendar": "agendar_visita",
            "otro": "react_agent",
        },
    )

    # Todos los caminos terminan en guardar_historial
    builder.add_edge("buscar_propiedades", "guardar_historial")
    builder.add_edge("comparar_propiedades", "guardar_historial")
    builder.add_edge("agendar_visita", "guardar_historial")
    builder.add_edge("react_agent", "guardar_historial")

    builder.set_finish_point("guardar_historial")

    return builder.compile()