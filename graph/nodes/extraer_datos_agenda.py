# Ruta: /REAL_ESTATE_AGENT/graph/nodes/extraer_datos_agenda.py

import re
import dateparser
from typing import Dict, Any
from tools.redis import guardar_contexto, recuperar_contexto

def extraer_datos_agenda_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extrae ID, fecha y hora. Limpia el texto antes de pasarlo a dateparser
    para evitar confusiones y acumula la información a través de turnos.
    """
    print("---🧩 NODO: EXTRAER DATOS DE AGENDA (v3 - Robusto)---")
    texto = state.get("pregunta", "").lower()
    usuario = state.get("usuario")

    # 1. Recuperar el contexto existente de Redis
    datos_previos = recuperar_contexto(usuario, "datos_visita") or {}
    print(f"Contexto previo recuperado: {datos_previos}")

    # 2. Extraer ID de Propiedad
    id_match = re.search(r'(?:id|propiedad|casa|depto|el)\s*#?(\d+)', texto)
    id_nuevo = int(id_match.group(1)) if id_match else None

    # --- CAMBIO CLAVE: Limpiar el texto para dateparser ---
    texto_para_fecha = texto
    if id_match:
        # Si encontramos un ID, lo quitamos del texto para no confundir a dateparser
        texto_para_fecha = texto.replace(id_match.group(0), "")
        print(f"Texto limpiado para dateparser: '{texto_para_fecha}'")

    # 3. Extraer Fecha y Hora del texto (limpio o completo)
    fecha_detectada = dateparser.parse(
        texto_para_fecha, 
        languages=['es'],
        settings={'PREFER_DATES_FROM': 'future', 'RETURN_AS_TIMEZONE_AWARE': False}
    )
    
    fecha_nueva = None
    hora_nueva = None
    if fecha_detectada:
        fecha_nueva = fecha_detectada.strftime("%d de %B de %Y")
        if fecha_detectada.hour != 0 or fecha_detectada.minute != 0:
            hora_nueva = fecha_detectada.strftime("%H:%M hs")
    
    print(f"Información nueva extraída: ID={id_nuevo}, Fecha={fecha_nueva}, Hora={hora_nueva}")

    # 4. Fusionar lo viejo con lo nuevo
    datos_fusionados = {
        "id_propiedad": id_nuevo or datos_previos.get("id_propiedad"),
        "fecha": fecha_nueva or datos_previos.get("fecha"),
        "hora": hora_nueva or datos_previos.get("hora")
    }
    print(f"Datos fusionados para la visita: {datos_fusionados}")

    # 5. Guardar y pasar el estado fusionado
    guardar_contexto(usuario, "datos_visita", datos_fusionados)
    return {"datos_visita": datos_fusionados}