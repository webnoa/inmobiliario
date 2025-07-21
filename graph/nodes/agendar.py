# Ruta: /REAL_ESTATE_AGENT/graph/nodes/agendar.py

from typing import Dict, Any

def agendar_visita_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Intenta agendar una visita. Si faltan datos, pide la información
    necesaria de forma conversacional.
    """
    print("---📅 NODO: AGENDAR VISITA (v2)---")
    datos_visita = state.get("datos_visita", {})

    propiedad_id = datos_visita.get("id_propiedad")
    fecha = datos_visita.get("fecha")
    hora = datos_visita.get("hora")

    # --- LÓGICA CONVERSACIONAL ---
    if not propiedad_id or not fecha or not hora:
        partes_faltantes = []
        if not propiedad_id:
            partes_faltantes.append("el ID de la propiedad")
        if not fecha:
            partes_faltantes.append("el día")
        if not hora:
            partes_faltantes.append("la hora")
        
        respuesta_texto = f"¡Casi lo tenemos! Para agendar, solo me falta que me digas {', '.join(partes_faltantes)}."
        return {"respuesta": respuesta_texto}

    # Si tenemos todos los datos, confirmamos
    respuesta_texto = (
        f"¡Perfecto! He agendado tu visita.\n\n"
        f"✅ **Propiedad ID**: {propiedad_id}\n"
        f"🗓️ **Fecha**: {fecha}\n"
        f"⏰ **Hora**: {hora}\n\n"
        f"Un asesor se pondrá en contacto contigo para confirmar. ¡Gracias!"
    )

    return {
        "datos_visita_confirmada": datos_visita,
        "respuesta": respuesta_texto
    }