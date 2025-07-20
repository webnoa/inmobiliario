
from tools.redis import recuperar_contexto
from tools.db import obtener_propiedades_por_ids
from typing import Dict

def _map_prop(p):
    # normaliza keys a (id, tipo, ambientes)
    return {
        "id": p.get("id"),
        "tipo": p.get("tipo") or p.get("type") or "Propiedad",
        "ambientes": p.get("ambientes") or p.get("rooms") or "?",
    }

def comparar_propiedades_node(state: Dict) -> Dict:
    usuario = state.get("usuario", "anonimo")
    input_data = state.get("input", {})

    ids = input_data.get("propiedades", [])

    if not ids:
        contexto = recuperar_contexto(usuario, "propiedades_encontradas")  # preferimos lista de props
        if contexto and isinstance(contexto, list):
            ids = [p.get("id") for p in contexto[:2] if p.get("id") is not None]
        else:
            # fallback vieja clave
            busq = recuperar_contexto(usuario, "ultima_busqueda") or {}
            cand_ids = busq.get("ids") if isinstance(busq, dict) else None
            if cand_ids:
                ids = cand_ids

    if len(ids) < 2:
        return {**state, "respuesta": "Necesito al menos dos propiedades para comparar."}

    propiedades = obtener_propiedades_por_ids(ids)
    if len(propiedades) < 2:
        return {**state, "respuesta": "No encontré suficientes propiedades para comparar."}

    p1, p2 = [_map_prop(x) for x in propiedades[:2]]
    comparacion = (
        f"Propiedad {p1['id']} ({p1['tipo']}, {p1['ambientes']} amb) vs "
        f"Propiedad {p2['id']} ({p2['tipo']}, {p2['ambientes']} amb)."
    )

    return {**state, "respuesta": comparacion}
