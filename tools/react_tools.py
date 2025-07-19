from langchain_core.tools import tool

@tool
def saludar(nombre: str) -> str:
    """Saluda al usuario por su nombre"""
    return f"Hola {nombre}, ¿en qué puedo ayudarte hoy?"

tools = [saludar]
