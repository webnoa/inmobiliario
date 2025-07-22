# Ruta: /REAL_ESTATE_AGENT/app_gradio.py

import gradio as gr
import requests
import uuid
import os

# --- Configuración ---
API_HOST = os.getenv("API_HOST", "http://api:8000")
API_URL = f"{API_HOST}/consulta_graph"

# --- Lógica de Comunicación con la API ---
def chatbot_response(message: str, session_id: str) -> str:
    """
    Envía el mensaje del usuario al backend de FastAPI y devuelve la respuesta.
    """
    if not message or not message.strip():
        return "Por favor, escribe una pregunta."

    params = {"q": message, "usuario": session_id}

    try:
        response = requests.get(API_URL, params=params, timeout=30) # Aumentamos el timeout
        response.raise_for_status()
        data = response.json()
        return data.get("respuesta_final", "Error: No se recibió una respuesta válida del servidor.")
    except requests.exceptions.RequestException as e:
        return f"Error de conexión con el backend en '{API_URL}'. El servidor podría estar ocupado. Error: {e}"

# --- Construcción de la Interfaz con Gradio ---
with gr.Blocks(theme=gr.themes.Soft(), title="Agente Inmobiliario") as demo:
    # Estado para mantener un ID de sesión único por usuario
    session_id = gr.State(value=str(uuid.uuid4()))
    
    gr.Markdown("# 🤖 Chat con el Agente Inmobiliario")

    # Chatbot configurado para el formato 'messages'
    chatbot = gr.Chatbot(
        label="Chat",
        height=600,
        bubble_full_width=False,
        type="messages" # <-- Formato correcto activado
    )

    # Textbox para la entrada del usuario
    msg = gr.Textbox(
        placeholder="Busca una casa en Yerba Buena...",
        label="Escribe tu consulta y presiona Enter"
    )

    # Botón para limpiar la conversación
    clear = gr.ClearButton([msg, chatbot], value="Limpiar Chat")

    # --- FUNCIÓN 'respond' QUE MANEJA EL FORMATO 'messages' ---
    def respond(message, chat_history, session_id_state):
        """
        Toma el mensaje del usuario, obtiene la respuesta del bot y actualiza
        el historial en el formato de diccionarios que Gradio espera.
        """
        # 1. Añade el mensaje del usuario al historial en el formato correcto
        chat_history.append({"role": "user", "content": message})
        
        # 2. Obtiene la respuesta del bot llamando a la API
        bot_message_content = chatbot_response(message, session_id_state)
        
        # 3. Añade la respuesta del bot al historial en el formato correcto
        chat_history.append({"role": "assistant", "content": bot_message_content})
        
        # 4. Devuelve una cadena vacía para limpiar el textbox y el historial actualizado
        return "", chat_history

    # Conecta el evento 'submit' del textbox a la función 'respond'
    msg.submit(respond, [msg, chatbot, session_id], [msg, chatbot])

if __name__ == "__main__":
    print(f"Iniciando la interfaz de Gradio...")
    print(f"Backend API URL: {API_URL}")
    demo.launch(server_name="0.0.0.0", server_port=7860)