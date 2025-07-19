from typing import TypedDict
from langchain.chat_models import ChatOpenAI
from tools.redis import guardar_en_historial
from datetime import datetime
from tools.intent_embeddings import clasificar_por_semantica

class GraphState(TypedDict):
    pregunta: str
    intencion: str
    respuesta: str
    usuario: str

def clasificar_intencion(state: GraphState) -> GraphState:
    pregunta = state["pregunta"].lower()
    usuario = state.get("usuario", "anonimo")

    if any(p in pregunta for p in ["alquilar", "vender", "venta", "comprar", "mostrar", "buscar", "casas", "deptos"]):
        intencion = "buscar"
        print("✔ Detectado por keyword → buscar")
    elif any(p in pregunta for p in ["comparar", "diferencias", "ventajas", "desventajas"]):
        intencion = "comparar"
        print("✔ Detectado por keyword → comparar")
    elif any(p in pregunta for p in ["agendar", "visitar", "cita", "turno"]):
        intencion = "agendar"
        print("✔ Detectado por keyword → agendar")
    else:
        intencion = clasificar_por_semantica(pregunta)
        print(f"✔ Detectado por embeddings → {intencion}")

    entrada = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "pregunta": pregunta,
        "intencion": intencion,
        "respuesta": "",
    }
    guardar_en_historial(usuario, pregunta, intencion, "")

    return {**state, "intencion": intencion}