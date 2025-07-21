# Ruta: /REAL_ESTATE_AGENT/graph/nodes/extraer_datos_agenda.py

import re
import dateparser
from typing import Dict, Any
from tools.redis import guardar_contexto, recuperar_contexto

def extraer_datos_agenda_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extrae ID, fecha y hora. Acumula la información a través de múltiples turnos
    usando Redis como memoria a corto plazo.
    """
    print("---🧩 NODO: EXTRAER DATOS DE AGENDA (v2)---")
    texto = state.get("pregunta", "").lower()
    usuario = state.get("usuario")

    # --- 1. RECUPERAR EL CONTEXTO EXISTENTE ---
    # Traemos lo que ya sabíamos de la visita desde Redis.
    datos_previos = recuperar_contexto(usuario, "datos_visita") or {}
    print(f"Contexto previo recuperado de Redis: {datos_previos}")

    # --- 2. EXTRAER NUEVA INFORMACIÓN DE LA PREGUNTA ACTUAL ---
    # Extraer ID
    id_match = re.search(r'(?:id|propiedad|casa|depto|el)\s*#?(\d+)', texto)
    id_nuevo = int(id_match.group(1)) if id_match else None
    
    # Extraer Fecha y Hora
    fecha_detectada = dateparser.parse(
        texto, 
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

    # --- 3. FUSIONAR LO VIEJO CON LO NUEVO ---
    # Creamos el estado final para la visita, dando prioridad a la información
    # recién extraída en este turno.
    datos_fusionados = {
        "id_propiedad": id_nuevo or datos_previos.get("id_propiedad"),
        "fecha": fecha_nueva or datos_previos.get("fecha"),
        "hora": hora_nueva or datos_previos.get("hora")
    }
    print(f"Datos fusionados para la visita: {datos_fusionados}")

    # --- 4. GUARDAR Y PASAR EL ESTADO FUSIONADO ---
    # Guardamos el estado completo y actualizado en Redis para el próximo turno.
    guardar_contexto(usuario, "datos_visita", datos_fusionados)

    # Pasamos el estado completo al siguiente nodo en el grafo.
    return {"datos_visita": datos_fusionados}