# Ruta: /REAL_ESTATE_AGENT/tools/intent_embeddings.py

import numpy as np
from openai import OpenAI
from scipy.spatial.distance import cosine
from typing import Dict, List

# Importamos la clave de API desde nuestro archivo de configuración central
from config import OPENAI_API_KEY

# Inicializamos el cliente de OpenAI una sola vez
client = OpenAI(api_key=OPENAI_API_KEY)

# --- 1. DICCIONARIO DE INTENCIONES CON EJEMPLOS RICOS ---
INTENT_EXAMPLES: Dict[str, List[str]] = {
    "buscar": [
        "busco casa en yerba buena",
        "muéstrame departamentos en el centro",
        "qué tenés en venta en tafí viejo",
        "hay algun loft en barrio norte",
        "necesito un alquiler de 2 ambientes",
        "propiedades con patio",
        "dame info de la casa 2", # Ejemplo añadido
    ],
    "favorito": [
        "agrega la propiedad 6",
        "añade la 3 a mis favoritos",
        "quiero guardar la casa con id 5",
        "guarda el depto 1",
        "muéstrame mis favoritos",
        "ver mi lista de favoritos",
        "quitar la 2 de favoritos",
        "elimina la propiedad 3",
    ],
    "otro": [
        "hola",
        "gracias",
        "quién eres tú",
        "cuál es la capital de francia",
        "jajaja qué gracioso",
        "ok",
        "perfecto",
        "cómo estás",
    ]
}

# --- 2. CACHÉ DE EMBEDDINGS ---
embedding_cache: Dict[str, np.ndarray] = {}

def get_embedding(text: str, model: str = "text-embedding-3-small") -> np.ndarray:
    """
    Obtiene el embedding para un texto dado, usando una caché para evitar
    llamadas repetidas a la API.
    """
    text = text.replace("\n", " ")
    if text in embedding_cache:
        return embedding_cache[text]
    
    try:
        response = client.embeddings.create(input=[text], model=model)
        embedding = np.array(response.data[0].embedding)
        embedding_cache[text] = embedding
        return embedding
    except Exception as e:
        print(f"🚨 Error al obtener embedding de OpenAI: {e}")
        return np.zeros(1536)

# --- 3. FUNCIÓN PRINCIPAL DE CLASIFICACIÓN ---
def clasificar_por_semantica(pregunta: str, umbral_confianza: float = 0.72) -> str:
    """
    Clasifica la pregunta del usuario encontrando la intención con la mayor
    similitud semántica, siempre que supere un umbral de confianza más flexible.
    """
    if not pregunta:
        return "otro"

    pregunta_embedding = get_embedding(pregunta)
    
    mejor_intencion = "otro"
    max_similitud = -1.0

    for intencion, ejemplos in INTENT_EXAMPLES.items():
        for ejemplo in ejemplos:
            ejemplo_embedding = get_embedding(ejemplo)
            similitud = 1 - cosine(pregunta_embedding, ejemplo_embedding)
            
            if similitud > max_similitud:
                max_similitud = similitud
                mejor_intencion = intencion

    print(f"Similitud máxima encontrada: {max_similitud:.2f} para la intención '{mejor_intencion}'")

    if max_similitud < umbral_confianza:
        print(f"La similitud no supera el umbral de {umbral_confianza}. Se clasifica como 'otro'.")
        return "otro"

    return mejor_intencion