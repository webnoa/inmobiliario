# Ruta: /REAL_ESTATE_AGENT/api/main.py

from fastapi import FastAPI, Query
from graph.property_graph import build_graph
from tools.redis import recuperar_historial, recuperar_contexto

# --- MEJORA DE RENDIMIENTO ---
# Construimos el grafo una sola vez cuando la aplicación se inicia.
# Esto evita el costo de reconstruir el grafo en cada petición.
app = FastAPI(title="API del Agente Inmobiliario")
graph = build_graph()

# --- ENDPOINT PRINCIPAL PARA GRADIO (CORREGIDO) ---
@app.get("/consulta_graph")
def consulta_por_grafo(q: str, usuario: str = "anonimo"):
    """
    Recibe una consulta y un usuario, ejecuta el grafo de LangGraph
    y devuelve la respuesta final en el formato esperado por el frontend.
    """
    # Define la entrada inicial para el grafo.
    # No es necesario pasar "intencion" o "respuesta" vacíos, el estado del grafo los manejará.
    inputs = {"pregunta": q, "usuario": usuario}

    # Invoca el grafo para obtener el estado final.
    final_state = graph.invoke(inputs)

    # Extrae la respuesta del estado final.
    # La clave 'respuesta' es donde tus nodos guardan el resultado para el usuario.
    final_answer = final_state.get("respuesta", "No se encontró una respuesta en el estado final.")

    # --- CAMBIO CLAVE ---
    # Empaqueta la respuesta en el formato que Gradio espera.
    return {"respuesta_final": final_answer}


# --- ENDPOINTS DE UTILIDAD (SIN CAMBIOS FUNCIONALES) ---

@app.get("/historial")
def ver_historial(usuario: str = "anonimo"):
    """Devuelve el historial de conversación para un usuario."""
    historial = recuperar_historial(usuario)
    return {"historial": historial}


@app.get("/ver_contexto")
def ver_contexto(usuario: str = "anonimo", campo: str = "datos_visita"):
    """Devuelve un campo específico del contexto de un usuario desde Redis."""
    contexto = recuperar_contexto(usuario, campo)
    return {"usuario": usuario, "campo": campo, "contexto": contexto}


@app.get("/flujo_demo_completo")
def flujo_demo_completo(usuario: str = "jose"):
    """
    Simula una conversación completa de varios turnos para un usuario.
    Usa la instancia global del grafo para mayor eficiencia.
    """
    interacciones = [
        "Busco una casa con patio",
        "¿Cuál me conviene más?",
        "Quiero agendar para mañana a las 18hs",
    ]
    resultados = []
    
    # El estado se construye en cada paso del bucle
    for pregunta in interacciones:
        inputs = {"pregunta": pregunta, "usuario": usuario}
        # El grafo gestiona y mantiene el estado internamente entre invocaciones
        # si se configura con una memoria persistente (como Redis).
        # Para una simulación simple, invocamos con la nueva pregunta.
        final_state = graph.invoke(inputs)
        resultados.append(final_state)
        
    return {"flujo_completado_para": usuario, "resultados_por_paso": resultados}