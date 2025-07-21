# Ruta: /REAL_ESTATE_AGENT/graph/property_graph.py

from typing import TypedDict, List, Dict, Any
from langgraph.graph import StateGraph
from graph.nodes.classifier import clasificar_intencion_node
from graph.nodes.search import buscar_propiedades_node
from graph.nodes.compare import comparar_propiedades_node
from graph.nodes.agendar import agendar_visita_node
from graph.nodes.react_agent import react_agent_node
from graph.nodes.historial import guardar_historial_node
from graph.nodes.extraer_datos_agenda import extraer_datos_agenda_node
from graph.nodes.preprocesar_contexto import preprocesar_contexto_node

# --- MEJORA: Definición de estado más completa ---
# Añadimos todas las claves que se usan a lo largo del grafo para mayor claridad.
class GraphState(TypedDict, total=False):
    pregunta: str
    intencion: str
    respuesta: str
    usuario: str
    propiedades_encontradas: List[Dict[str, Any]]
    datos_visita: Dict[str, Any]
    datos_visita_confirmada: Dict[str, Any]

def build_graph():
    """
    Construye y compila el grafo de LangGraph con todos los nodos y flujos lógicos.
    """
    workflow = StateGraph(GraphState)

    # Añadir todos los nodos al grafo
    workflow.add_node("clasificar_intencion", clasificar_intencion_node)
    workflow.add_node("buscar_propiedades", buscar_propiedades_node)
    workflow.add_node("comparar_propiedades", comparar_propiedades_node)
    workflow.add_node("extraer_datos_agenda", extraer_datos_agenda_node)
    workflow.add_node("agendar_visita", agendar_visita_node)
    workflow.add_node("preprocesar_contexto", preprocesar_contexto_node)
    workflow.add_node("react_agent", react_agent_node)
    workflow.add_node("guardar_historial", guardar_historial_node)

    # Definir el punto de entrada
    workflow.set_entry_point("clasificar_intencion")

    # Definir las rutas condicionales basadas en la intención
    workflow.add_conditional_edges(
        "clasificar_intencion",
        lambda state: state.get("intencion"),
        {
            "buscar": "buscar_propiedades",
            "comparar": "comparar_propiedades",
            "agendar": "extraer_datos_agenda",
            "otro": "preprocesar_contexto",
        },
    )

    # Definir las rutas fijas
    workflow.add_edge("extraer_datos_agenda", "agendar_visita")
    workflow.add_edge("preprocesar_contexto", "react_agent")

    # Definir las rutas hacia el nodo final
    workflow.add_edge("buscar_propiedades", "guardar_historial")
    workflow.add_edge("comparar_propiedades", "guardar_historial")
    workflow.add_edge("agendar_visita", "guardar_historial")
    workflow.add_edge("react_agent", "guardar_historial")

    # Definir el punto final del grafo
    workflow.set_finish_point("guardar_historial")

    # Compilar el grafo y devolverlo
    return workflow.compile()