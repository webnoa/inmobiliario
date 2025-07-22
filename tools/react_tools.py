# Ruta: /REAL_ESTATE_AGENT/tools/react_tools.py

from langchain.agents import tool, create_react_agent, AgentExecutor
from langchain_community.chat_models import ChatOpenAI
from langchain import hub
from typing import Dict, Any

# Importamos las funciones de Redis y DB para que las herramientas puedan usarlas
from .redis import guardar_contexto, recuperar_contexto, recuperar_historial
from .db import obtener_propiedades_por_ids
# ... (imports existentes)
from langchain_qdrant import Qdrant
from langchain_openai import OpenAIEmbeddings
from qdrant_client import QdrantClient
from config import OPENAI_API_KEY
# --- Definición de Herramientas para el Agente ReAct ---

@tool
def saludar(usuario: str) -> str:
    """Saluda al usuario, intentando usar su nombre si está guardado en el contexto."""
    nombre_guardado = recuperar_contexto(usuario, "nombre_usuario")
    if nombre_guardado:
        return f"¡Hola, {nombre_guardado}! Qué bueno verte de nuevo. ¿En qué te puedo ayudar hoy?"
    return "¡Hola! Soy tu asistente inmobiliario. ¿En qué puedo ayudarte?"

@tool
def recordar_nombre_usuario(nombre: str, usuario: str) -> str:
    """Guarda el nombre del usuario para futuras interacciones."""
    guardar_contexto(usuario, "nombre_usuario", nombre)
    return f"¡Mucho gusto, {nombre}! He guardado tu nombre. ¿En qué puedo ayudarte?"

@tool
def buscar_ultima_busqueda(usuario: str) -> str:
    """Busca y resume la última búsqueda de propiedades realizada por un usuario."""
    ultima_busqueda = recuperar_contexto(usuario, "ultima_busqueda")
    if ultima_busqueda and isinstance(ultima_busqueda, dict):
        texto_busqueda = ultima_busqueda.get("texto", "una búsqueda anterior")
        return f"Tu última búsqueda fue sobre: '{texto_busqueda}'. ¿Quieres continuar con eso?"
    return "No tengo registrada una búsqueda reciente para ti. ¿Qué te gustaría buscar?"

# --- NUEVA HERRAMIENTA ---
@tool
def obtener_detalles_propiedad(id_propiedad: int) -> str:
    """
    Busca y devuelve los detalles completos de una única propiedad usando su ID.
    Es útil si el usuario pregunta 'muéstrame la propiedad 6' o 'dame detalles del ID 3'.
    """
    try:
        propiedades = obtener_propiedades_por_ids([id_propiedad])
        if not propiedades:
            return f"No encontré ninguna propiedad con el ID {id_propiedad} en la base de datos."
        
        prop = propiedades[0]
        detalles = (
            f"¡Claro! Aquí tienes los detalles de la Propiedad ID {prop.get('id')}:\n"
            f"- Título: {prop.get('title', 'N/A')}\n"
            f"- Tipo: {prop.get('type', 'N/A').capitalize()}\n"
            f"- Ubicación: {prop.get('location', 'N/A')}\n"
            f"- Precio: ${prop.get('price', 0):,}\n"
            f"- Ambientes: {prop.get('rooms', 'N/A')}\n"
            f"- Superficie: {prop.get('area_m2', 'N/A')} m²"
        )
        return detalles
    except Exception as e:
        print(f"🚨 Error en la herramienta obtener_detalles_propiedad: {e}")
        return "Tuve un problema al buscar los detalles de esa propiedad en la base de datos."

@tool
def respuesta_por_defecto(pregunta_original: str) -> str:
    """Úsalo como último recurso cuando ninguna otra herramienta sea apropiada."""
    return "Lo siento, no estoy seguro de cómo ayudarte con eso. Soy un asistente inmobiliario. Puedo buscar, comparar o agendar visitas a propiedades. ¿Cómo te gustaría proceder?"

# --- Lista de Herramientas y Prompt ---
# --- NUEVA Y POTENTE HERRAMIENTA RAG ---
@tool
def buscar_detalles_en_documentos(pregunta_especifica: str) -> str:
    """
    Busca en la base de datos de documentos (Vectorstore) para encontrar respuestas
    a preguntas específicas sobre una propiedad que no se encuentran en la base de
    datos principal. Úsalo para preguntas como '¿cuáles son las expensas?',
    '¿se permiten mascotas?' o '¿qué dice el reglamento?'.
    """
    print(f"---🧠 HERRAMIENTA RAG: Buscando respuesta para: '{pregunta_especifica}'---")
    try:
        # 1. Conectar al cliente de Qdrant
        client = QdrantClient(host="qdrant", port=6333) # Usamos el nombre del servicio de Docker
        
        # 2. Inicializar el modelo de embeddings
        embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY, model="text-embedding-3-small")
        
        # 3. Conectar a la colección existente en Qdrant
        vector_store = Qdrant(
            client=client,
            collection_name="propiedades_detalles",
            embeddings=embeddings,
        )
        
        # 4. Realizar la búsqueda de similitud
        # Busca los 3 fragmentos más relevantes para la pregunta del usuario
        documentos_encontrados = vector_store.similarity_search(pregunta_especifica, k=3)
        
        if not documentos_encontrados:
            return "No encontré información sobre eso en los documentos de la propiedad."
            
        # 5. Formatear la respuesta
        # Unimos el contenido de los fragmentos encontrados para dar contexto al LLM
        contexto = "\n\n---\n\n".join([doc.page_content for doc in documentos_encontrados])
        
        # (Opcional pero recomendado) Podríamos pasar esto a un LLM para una respuesta más elaborada,
        # pero por ahora, devolver el contexto crudo es un excelente primer paso.
        return f"Encontré esta información relevante en los documentos: {contexto}"

    except Exception as e:
        print(f"🚨 Error en la herramienta buscar_detalles_en_documentos: {e}")
        return "Tuve un problema al consultar la base de datos de documentos."
    


# --- Actualizar la Lista de Herramientas ---
TOOLS = [
    saludar,
    recordar_nombre_usuario,
    buscar_ultima_busqueda,
    obtener_detalles_propiedad,
    buscar_detalles_en_documentos, # <-- Nueva herramienta RAG
    respuesta_por_defecto,
]

PROMPT = hub.pull("hwchase17/react")

# --- Fábrica del Agente ---
def crear_agente_react() -> AgentExecutor:
    llm = ChatOpenAI(model="gpt-4o", temperature=0, streaming=True)
    agent = create_react_agent(llm=llm, tools=TOOLS, prompt=PROMPT)
    agent_executor = AgentExecutor(
        agent=agent, tools=TOOLS, verbose=True,
        max_iterations=5, handle_parsing_errors=True
    )
    return agent_executor