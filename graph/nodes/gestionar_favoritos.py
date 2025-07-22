# Ruta: /REAL_ESTATE_AGENT/graph/nodes/gestionar_favoritos.py

import re
from typing import Dict, Any
from tools.redis import guardar_contexto, recuperar_contexto
from tools.db import obtener_propiedades_por_ids

def gestionar_favoritos_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Gestiona la lista de favoritos. Infiere la intención de añadir si la
    pregunta es corta y el contexto previo es de favoritos.
    """
    print("---❤️ NODO: GESTIONAR FAVORITOS (v3 - Proactivo)---")
    pregunta = state.get("pregunta", "").lower()
    usuario = state.get("usuario")
    
    favoritos_actuales = recuperar_contexto(usuario, "favoritos") or []
    ids_mencionados = [int(id_str) for id_str in re.findall(r'\d+', pregunta)]
    
    # --- LÓGICA DE INFERENCIA DE ACCIÓN ---
    accion = "listar" # Por defecto, listamos
    
    # Determinar la acción explícita
    if any(word in pregunta for word in ["añadir", "guarda", "agregar"]):
        accion = "añadir"
    elif any(word in pregunta for word in ["quitar", "eliminar", "borrar"]):
        accion = "quitar"
    
    # --- CAMBIO CLAVE: Inferencia por contexto ---
    # Si la pregunta es corta, contiene un ID y no tiene un verbo claro,
    # pero la última intención fue 'favorito', asumimos que quiere añadir.
    ultima_intencion = recuperar_contexto(usuario, "ultima_intencion") or {}
    if (len(pregunta.split()) <= 4 and ids_mencionados and 
        ultima_intencion.get("intencion") == "favorito" and 
        accion == "listar"): # Solo si no se detectó otra acción
        
        print("Inferencia activada: El usuario probablemente quiere añadir al favorito anterior.")
        accion = "añadir"

    # --- EJECUCIÓN DE LA ACCIÓN ---
    if accion == "añadir":
        if not ids_mencionados:
            return {"respuesta": "Claro, dime el ID de la propiedad que quieres añadir a favoritos."}
        
        nuevos_favoritos = sorted(list(set(favoritos_actuales + ids_mencionados)))
        guardar_contexto(usuario, "favoritos", nuevos_favoritos)
        return {"respuesta": f"¡Hecho! He añadido las propiedades con ID {', '.join(map(str, ids_mencionados))} a tus favoritos. Ahora tienes {len(nuevos_favoritos)} propiedades guardadas."}

    elif accion == "quitar":
        if not ids_mencionados:
            return {"respuesta": "Claro, dime el ID de la propiedad que quieres quitar de tus favoritos."}
            
        favoritos_actualizados = [fav for fav in favoritos_actuales if fav not in ids_mencionados]
        guardar_contexto(usuario, "favoritos", favoritos_actualizados)
        return {"respuesta": f"Listo. He quitado las propiedades con ID {', '.join(map(str, ids_mencionados))} de tus favoritos."}

    else: # Acción por defecto: listar
        if not favoritos_actuales:
            return {"respuesta": "Aún no tienes ninguna propiedad guardada en tus favoritos."}
        
        detalles_favoritos = obtener_propiedades_por_ids(favoritos_actuales)
        if not detalles_favoritos:
            return {"respuesta": "Parece que tus propiedades favoritas ya no están disponibles."}

        respuesta_texto = "Aquí tienes tu lista de propiedades favoritas:\n\n"
        for prop in detalles_favoritos:
            respuesta_texto += f"**ID {prop.get('id')}**: {prop.get('title', 'Sin título')}\n"
        
        return {"respuesta": respuesta_texto}