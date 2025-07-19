from typing import TypedDict
import re
from datetime import datetime

class GraphState(TypedDict):
    pregunta: str
    intencion: str
    respuesta: str
    usuario: str

def agendar_visita_node(state: GraphState) -> GraphState:
    pregunta = state["pregunta"].lower()

    # Buscar fecha y hora en el texto con regex (simplificado)
    fecha = re.search(r"(lunes|martes|miércoles|jueves|viernes|sábado|domingo|hoy|mañana)", pregunta)
    hora = re.search(r"(\d{1,2})(?:\s*hs|:\d{2})?", pregunta)

    texto_fecha = fecha.group(0) if fecha else "una fecha a coordinar"
    texto_hora = hora.group(0) + "hs" if hora else "un horario a confirmar"

    confirmacion = f"✅ Visita agendada para {texto_fecha} a las {texto_hora}. Te estaremos contactando para confirmar."

    print(f"📅 Agendando visita para {state['usuario']}: {texto_fecha} - {texto_hora}")

    return {
        "pregunta": state["pregunta"],
        "intencion": state["intencion"],
        "respuesta": confirmacion,
        "usuario": state["usuario"]
    }
