
from typing import TypedDict
from langgraph.graph import StateGraph
from graph.nodes.classifier import clasificar_intencion
from graph.nodes.search import buscar_propiedades_node
from graph.nodes.compare import comparar_propiedades_node
from graph.nodes.agenda import agendar_visita_node
from graph.nodes.react_agent import react_agent_node
from graph.nodes.historial import guardar_historial_node
from graph.nodes.extraer_datos_agenda import extraer_datos_agenda_node
from graph.nodes.preprocesar_contexto import preprocesar_contexto_node

class GraphState(TypedDict, total=False):
    pregunta: str
    intencion: str
    respuesta: str
    usuario: str
    input: dict

def build_graph():
    builder = StateGraph(GraphState)

    builder.add_node("clasificar_intencion", clasificar_intencion)
    builder.add_node("buscar_propiedades", buscar_propiedades_node)
    builder.add_node("comparar_propiedades", comparar_propiedades_node)
    builder.add_node("extraer_datos_agenda", extraer_datos_agenda_node)
    builder.add_node("agendar_visita", agendar_visita_node)
    builder.add_node("preprocesar_contexto", preprocesar_contexto_node)
    builder.add_node("react_agent", react_agent_node)
    builder.add_node("guardar_historial", guardar_historial_node)

    builder.set_entry_point("clasificar_intencion")

    builder.add_conditional_edges(
        "clasificar_intencion",
        lambda state: state["intencion"],
        {
            "buscar": "buscar_propiedades",
            "comparar": "comparar_propiedades",
            "agendar": "extraer_datos_agenda",
            "otro": "preprocesar_contexto",  # pasa por preprocesador antes del agente
        },
    )

    builder.add_edge("extraer_datos_agenda", "agendar_visita")
    builder.add_edge("preprocesar_contexto", "react_agent")

    builder.add_edge("buscar_propiedades", "guardar_historial")
    builder.add_edge("comparar_propiedades", "guardar_historial")
    builder.add_edge("agendar_visita", "guardar_historial")
    builder.add_edge("react_agent", "guardar_historial")

    builder.set_finish_point("guardar_historial")

    return builder.compile()
