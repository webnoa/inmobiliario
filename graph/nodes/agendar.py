
from typing import TypedDict
import re
from datetime import datetime
from tools.redis import recuperar_contexto, guardar_contexto

class GraphState(TypedDict, total=False):
    pregunta: str
    intencion: str
    respuesta: str
    usuario: str

def agendar_visita_node(state: GraphState) -> GraphState:
    usuario = state.get("usuario", "anonimo")
    pregunta = state.get("pregunta", "").lower()

    # 1) Intentar usar datos previamente extraídos
    ctx = recuperar_contexto(usuario, "datos_visita") or {}

    fecha = ctx.get("fecha")
    hora = ctx.get("hora")
    prop = ctx.get("propiedad_id")

    # 2) Fallback: regex rápida si no vino del extractor (por compatibilidad)
    if not fecha and "hoy" in pregunta:
        fecha = datetime.now().strftime("%Y-%m-%d")
    elif not fecha and "mañana" in pregunta:
        fecha = (datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
                 + timedelta(days=1)).strftime("%Y-%m-%d")

    if not hora:
        m_h = re.search(r"(\d{1,2})(?:[:h](\d{2}))?", pregunta)
        if m_h:
            h = int(m_h.group(1))
            m = int(m_h.group(2) or 0)
            hora = f"{h:02d}:{m:02d}"

    if not prop:
        m_p = re.search(r"(casa|propiedad|departamento)\s*(\d+)", pregunta)
        if m_p:
            prop = int(m_p.group(2))

    if not (fecha and hora and prop):
        return {**state, "respuesta": "❌ Necesito fecha, hora e ID de propiedad para agendar."}

    # persistimos confirmación
    guardar_contexto(usuario, "datos_visita_confirmada", {
        "fecha": fecha, "hora": hora, "propiedad_id": prop
    })

    mensaje = f"✅ Visita agendada para la propiedad {prop} el {fecha} a las {hora}."
    print(f"📅 Agendando visita ({usuario}): {mensaje}")
    return {**state, "respuesta": mensaje}
