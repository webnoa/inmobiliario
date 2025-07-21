from typing import Optional, Any, Dict, List
from langchain_community.chat_models import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from tools.redis import recuperar_contexto, recuperar_historial
from langchain import hub


# -------------------- TOOLS --------------------

@tool
def saludar(nombre: str) -> str:
    """Saluda al usuario por su nombre."""
    return f"Hola {nombre}, ¿en qué puedo ayudarte hoy?"

@tool
def buscar_ultima_busqueda(usuario: str) -> str:
    """Devuelve un listado corto de la última búsqueda de propiedades del usuario (si existe)."""
    props = recuperar_contexto(usuario, "propiedades_encontradas") or []
    if not props:
        return "No tengo propiedades recientes para este usuario."
    lineas = []
    for p in props[:5]:
        titulo = p.get("title") or p.get("titulo") or f"Propiedad {p.get('id','?')}"
        ubic = p.get("ubicacion") or p.get("location") or "Ubicación?"
        precio = p.get("precio") or p.get("price") or "?"
        lineas.append(f"{titulo} - {ubic} - USD {precio}")
    return "\n".join(lineas)

@tool
def resumen_historial(usuario: str, n: int = 3) -> str:
    """Devuelve las últimas N interacciones del historial del usuario."""
    hist = recuperar_historial(usuario)
    if not hist:
        return "Sin historial."
    sel = hist[:n]
    return "\n".join(
        f"[{h['timestamp']}] {h['pregunta']} → {h['intencion']}" for h in sel
    )

TOOLS = [saludar, buscar_ultima_busqueda, resumen_historial]

# Este prompt ya contiene las variables requeridas '{tools}' y '{tool_names}'.
PROMPT = hub.pull("hwchase17/react")

# --- Función para crear el Agente ---
def crear_agente_react():
    """
    Crea y devuelve un agente ReAct con las herramientas y el prompt configurados.
    """
    # ... (tu código para definir las herramientas 'TOOLS' debería estar aquí) ...
    # ... (tu código para definir el 'llm' debería estar aquí) ...
    llm = ChatOpenAI(model="gpt-4o", temperature=0) # Asumo que esto ya lo tienes

    # El resto de la función no necesita cambios, ya que ahora el PROMPT es correcto.
    agent = create_react_agent(llm=llm, tools=TOOLS, prompt=PROMPT)
    
    agent_executor = AgentExecutor(
        agent=agent,
        tools=TOOLS,
        verbose=True,
        # Esto es importante para que no se quede en un bucle infinito
        max_iterations=5, 
        handle_parsing_errors=True # Maneja errores si el LLM responde mal
    )
    return agent_executor