from tools.db import buscar_propiedades
from tools.redis import guardar_contexto, recuperar_contexto
from typing import Dict

def buscar_propiedades_node(state: Dict) -> Dict:
    pregunta = state.get("pregunta")
    usuario = state.get("usuario", "anonimo")

    if not pregunta:
        ctx = recuperar_contexto(usuario, "ultima_busqueda")
        if ctx:
            pregunta = ctx.get("texto", "")

    respuesta = buscar_propiedades(pregunta)

    if respuesta:
        guardar_contexto(usuario, "ultima_busqueda", {"texto": pregunta})
        guardar_contexto(usuario, "propiedades_encontradas", respuesta)

    texto = "\n".join([
    f"{p.get('titulo', p.get('title', 'Propiedad'))} - {p.get('ubicacion', 'Ubicación desconocida')} - USD {p.get('precio', 0)}"
    for p in respuesta
])

    return {**state, "respuesta": texto}
