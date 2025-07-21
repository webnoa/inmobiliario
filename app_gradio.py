# Ruta: /REAL_ESTATE_AGENT/app_gradio.py

import gradio as gr
import requests
import uuid
import os

# Lee la URL del backend desde una variable de entorno
API_HOST = os.getenv("API_HOST", "http://api:8000")
API_URL = f"{API_HOST}/consulta_graph"

def chatbot_response(message: str, history: list) -> str:
    """
    Envía el mensaje del usuario al backend de FastAPI y devuelve la respuesta.
    'history' ahora contiene el ID de sesión que inyectaremos.
    """
    # Extraemos el ID de sesión del estado del historial
    session_id = history[0] if history and isinstance(history[0], str) else str(uuid.uuid4())

    if not message or not message.strip():
        return "Por favor, escribe una pregunta."

    params = {
        "q": message,
        "usuario": session_id
    }

    try:
        response = requests.get(API_URL, params=params, timeout=20)
        response.raise_for_status()
        data = response.json()
        return data.get("respuesta_final", "Error: No se recibió una respuesta válida.")
    except requests.exceptions.HTTPError as e:
        return f"Error en API: {e.response.status_code} - {e.response.text}"
    except requests.exceptions.RequestException as e:
        return f"Error de conexión con el backend en '{API_URL}'. Error: {e}"

# --- Construcción de la Interfaz con Gradio (MODIFICADA) ---

# --- Construcción de la Interfaz con Gradio ---
with gr.Blocks(theme=gr.themes.Soft(), title="Agente Inmobiliario") as demo:
    # ... (la definición de session_id, Markdown, chatbot, msg, clear no cambia) ...
    session_id = gr.State(value=str(uuid.uuid4()))
    gr.Markdown("# 🤖 Chat con el Agente Inmobiliario")
    chatbot = gr.Chatbot(
        label="Chat",
        height=600,
        # type="messages" # <-- Eliminamos temporalmente para simplificar
    )
    msg = gr.Textbox(
        placeholder="Busca pisos en Barcelona con 3 habitaciones...",
        label="Escribe tu consulta y presiona Enter"
    )
    clear = gr.ClearButton([msg, chatbot], value="Limpiar Chat")

 # --- FUNCIÓN 'respond' CORREGIDA ---
    def respond(message, chat_history, session_id_state):
        """
        Toma el mensaje del usuario y el historial, obtiene la respuesta del bot
        y actualiza el historial en el formato correcto para Gradio.
        """
        # Llama a la función que se comunica con la API
        bot_message = chatbot_response(message, [session_id_state])
        
        # Añade el nuevo par de mensajes (usuario, bot) al historial
        chat_history.append((message, bot_message))
        
        # Devuelve una cadena vacía para limpiar el textbox y el historial actualizado
        return "", chat_history


    # Conecta el envío del mensaje del textbox a la función 'respond'
    msg.submit(respond, [msg, chatbot, session_id], [msg, chatbot])


if __name__ == "__main__":
    print(f"Iniciando la interfaz de Gradio...")
    print(f"Backend API URL: {API_URL}")
    demo.launch(server_name="0.0.0.0", server_port=7860)