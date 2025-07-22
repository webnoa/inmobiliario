# Ruta: /REAL_ESTATE_AGENT/graph/nodes/limpiar_contexto_visita.py

from typing import Dict, Any
from tools.redis import guardar_contexto

def limpiar_contexto_visita_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Nodo que limpia el contexto de la visita en Redis después de una
    confirmación exitosa.
    """
    print("---🧹 NODO: LIMPIAR CONTEXTO DE VISITA---")
    usuario = state.get("usuario")
    
    if usuario and state.get("datos_visita_confirmada"):
        # Sobrescribimos el contexto con un diccionario vacío para limpiarlo
        guardar_contexto(usuario, "datos_visita", {})
        print(f"Contexto 'datos_visita' limpiado para el usuario {usuario}.")
        
    # Este nodo no modifica la respuesta al usuario, solo el estado de fondo.
    # Devolvemos un diccionario vacío para no alterar otras partes del estado.
    return {}