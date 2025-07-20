
import re
from tools.react_tools import crear_agente_react, saludar
from tools.redis import guardar_contexto, recuperar_contexto

_NOMBRE_PATTERNS = [
    r"me llamo\s+(\w+)",
    r"mi nombre es\s+(\w+)",
    r"soy\s+(\w+)",
]

def _extraer_nombre(texto: str) -> str:
    t = texto.lower()
    for pat in _NOMBRE_PATTERNS:
        m = re.search(pat, t)
        if m:
            return m.group(1).capitalize()
    return ""

def react_agent_node(state: dict) -> dict:
    usuario = state.get("usuario", "anonimo")
    pregunta = state.get("pregunta", "").strip()

    # persistimos la pregunta
    guardar_contexto(usuario, "ultima_pregunta", {"texto": pregunta})

    # si el usuario se presenta -> responder directo sin LLM costoso
    nombre = _extraer_nombre(pregunta)
    if nombre:
        guardar_contexto(usuario, "nombre", {"valor": nombre})
        return {**state, "respuesta": saludar.run(nombre)}

    # si ya conocemos el nombre y la pregunta es solo saludo
    if pregunta.lower() in {"hola", "hola!", "hola.", "buenas", "buen día", "buenas tardes"}:
        ctx_nombre = recuperar_contexto(usuario, "nombre") or {}
        if ctx_nombre.get("valor"):
            return {**state, "respuesta": saludar.run(ctx_nombre["valor"])}

    # de lo contrario -> agente ReAct
    executor = crear_agente_react()
    result = executor.invoke({"input": pregunta, "usuario": usuario})
    # AgentExecutor may return dict or str
    if isinstance(result, dict):
        salida = result.get("output") or str(result)
    else:
        salida = str(result)

    return {**state, "respuesta": salida}
