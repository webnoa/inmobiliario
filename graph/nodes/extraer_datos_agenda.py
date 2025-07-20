from typing import TypedDict
import re
import dateparser

class GraphState(TypedDict):
    pregunta: str
    intencion: str
    respuesta: str
    usuario: str

from tools.redis import guardar_contexto

def extraer_datos_agenda_node(state: GraphState) -> GraphState:
    texto = state["pregunta"].lower()
    usuario = state["usuario"]

    fecha_detectada = dateparser.parse(texto, languages=["es"])
    hora_match = re.search(r"(\d{1,2})(?:\s*hs|:\d{2})", texto)
    id_match = re.search(r"(casa|departamento|propiedad)\s*(\d+)", texto)

    fecha = fecha_detectada.strftime("%Y-%m-%d") if fecha_detectada else None
    hora = hora_match.group(0) if hora_match else None
    propiedad_id = int(id_match.group(2)) if id_match else None

    datos = {}
    if fecha: datos["fecha"] = fecha
    if hora: datos["hora"] = hora
    if propiedad_id: datos["propiedad_id"] = propiedad_id

    if datos:
        guardar_contexto(usuario, "datos_visita", datos)

    return state
