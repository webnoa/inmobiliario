# Ruta: /REAL_ESTATE_AGENT/graph/property_graph.py

from typing import TypedDict, List, Dict, Any
from langgraph.graph import StateGraph

# Importación de todos los nodos
from graph.nodes.classifier import clasificar_intencion_node
from graph.nodes.search import buscar_propiedades_node
from graph.nodes.compare import comparar_propiedades_node
from graph.nodes.agendar import agendar_visita_node
from graph.nodes.react_agent import react_agent_node
from graph.nodes.historial import guardar_historial_node
from graph.nodes.extraer_datos_agenda import extraer_datos_agenda_node
from graph.nodes.preprocesar_contexto import preprocesar_contexto_node
from graph.nodes.limpiar_contexto_visita import limpiar_contexto_visita_node
from graph.nodes.gestionar_favoritos import gestionar_favoritos_node

# Definición completa del estado del grafo
class GraphState(TypedDict, total=False):
    pregunta: str
    intencion: str
    respuesta: str
    usuario: str
    propiedades_encontradas: List[Dict[str, Any]]
    datos_visita: Dict[str, Any]
    datos_visita_confirmada: Dict[str, Any]
    favoritos: List[int]

def build_graph():
    """
    Construye y compila el grafo de LangGraph con un flujo lógico corregido
    para evitar la interferencia del preprocesador de contexto.
    """
    workflow = StateGraph(GraphState)

    # Añadir todos los nodos al grafo (sin cambios aquí)
    workflow.add_node("clasificar_intencion", clasificar_intencion_node)
    workflow.add_node("buscar_propiedades", buscar_propiedades_node)
    workflow.add_node("comparar_propiedades", comparar_propiedades_node)
    workflow.add_node("extraer_datos_agenda", extraer_datos_agenda_node)
    workflow.add_node("agendar_visita", agendar_visita_node)
    workflow.add_node("preprocesar_contexto", preprocesar_contexto_node)
    workflow.add_node("react_agent", react_agent_node)
    workflow.add_node("guardar_historial", guardar_historial_node)
    workflow.add_node("limpiar_contexto_visita", limpiar_contexto_visita_node)
    workflow.add_node("gestionar_favoritos", gestionar_favoritos_node)

    # Definir el punto de entrada
    workflow.set_entry_point("clasificar_intencion")

    # --- LÓGICA DE ENRUTAMIENTO PRINCIPAL ---
    # Las intenciones que pueden tener preguntas de seguimiento ambiguas (como 'comparar'
    # o 'agendar') se envían primero al preprocesador de contexto.
    workflow.add_conditional_edges(
        "clasificar_intencion",
        lambda state: state.get("intencion"),
        {
            "favorito": "gestionar_favoritos",
            "buscar": "buscar_propiedades",
            # --- RUTAS MODIFICADAS para usar el contexto ---
            "comparar": "preprocesar_contexto",
            "agendar": "preprocesar_contexto",
            # --- Ruta sin cambios ---
            "otro": "react_agent",
        },
    )

    # --- NUEVA LÓGICA DE ENRUTAMIENTO DESPUÉS DEL PREPROCESADOR ---
    # Después de que el contexto ha sido (potencialmente) añadido,
    # enrutamos a la acción final basándonos en la misma intención original.
    workflow.add_conditional_edges(
        "preprocesar_contexto",
        lambda state: state.get("intencion"),
        {
            "comparar": "comparar_propiedades",
            "agendar": "extraer_datos_agenda",
        })
    
    workflow.add_edge("extraer_datos_agenda", "agendar_visita")

    def decidir_despues_de_agendar(state):
        return "limpiar_contexto" if state.get("datos_visita_confirmada") else "no_limpiar"

    workflow.add_conditional_edges(
        "agendar_visita",
        decidir_despues_de_agendar,
        {"limpiar_contexto": "limpiar_contexto_visita", "no_limpiar": "guardar_historial"}
    )
    
    # --- RUTAS HACIA EL NODO FINAL ---
    workflow.add_edge("limpiar_contexto_visita", "guardar_historial")
    workflow.add_edge("buscar_propiedades", "guardar_historial")
    workflow.add_edge("comparar_propiedades", "guardar_historial")
    workflow.add_edge("gestionar_favoritos", "guardar_historial")
    # La ruta desde react_agent al final sigue siendo necesaria
    workflow.add_edge("react_agent", "guardar_historial")

    # Definir el punto final del grafo
    workflow.set_finish_point("guardar_historial")

    # Compilar el grafo y devolverlo
    return workflow.compile()