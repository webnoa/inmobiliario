
"""Herramientas y helper para crear un agente ReAct simple.

El agente usa:
- Herramienta `saludar(nombre:str)`
- Herramienta `buscar_ultima_busqueda(usuario:str)` -> lee de Redis
- Herramienta `resumen_historial(usuario:str, n:int=3)` -> últimos n turnos
"""
from typing import Optional, Any, Dict, List
from langchain_community.chat_models import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from tools.redis import recuperar_contexto, recuperar_historial

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

# -------------------- PROMPT --------------------
_SYSTEM = (
    "Eres un asistente inmobiliario ReAct. Razona brevemente, decide si usar una herramienta, " 
    "y responde al usuario en español. Si la consulta requiere datos previos del usuario, usa las herramientas."
)

_HUMAN = "{input}"
_SCRATCH = "{agent_scratchpad}"

PROMPT = ChatPromptTemplate.from_messages([
    ("system", _SYSTEM),
    ("user", _HUMAN),
    ("assistant", _SCRATCH),
])

# -------------------- FACTORY --------------------
def crear_agente_react(llm: Optional[Any] = None) -> AgentExecutor:
    if llm is None:
        llm = ChatOpenAI(model="gpt-4o", temperature=0)
    agent = create_react_agent(llm=llm, tools=TOOLS, prompt=PROMPT)
    return AgentExecutor(agent=agent, tools=TOOLS, verbose=False)
