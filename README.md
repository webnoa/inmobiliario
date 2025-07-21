# 🤖 Agente Inmobiliario Inteligente con LangGraph

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-green?style=for-the-badge&logo=fastapi)
![LangChain](https://img.shields.io/badge/LangChain-LangGraph-orange?style=for-the-badge)
![Docker](https://img.shields.io/badge/Docker-Compose-blue?style=for-the-badge&logo=docker)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue?style=for-the-badge&logo=postgresql)
![Redis](https://img.shields.io/badge/Redis-7-red?style=for-the-badge&logo=redis)

Este proyecto implementa un agente conversacional avanzado para el sector inmobiliario. Utilizando un grafo de estados construido con **LangGraph**, el agente es capaz de entender las intenciones del usuario, realizar búsquedas en una base de datos, comparar propiedades, responder preguntas abiertas y agendar visitas de forma conversacional.

## ✨ Características Principales

- **Procesamiento de Intenciones Múltiples**: El agente utiliza un clasificador híbrido (keywords + embeddings semánticos) para determinar si el usuario quiere `buscar`, `comparar`, `agendar` o tener una conversación general.
- **Búsqueda Inteligente**: Realiza búsquedas en una base de datos **PostgreSQL** real, filtrando por términos clave y normalizando las consultas del usuario (ej: "casas" -> "casa").
- **Comparación de Propiedades**: Puede comparar propiedades específicas por su ID, buscando primero en el contexto de la conversación y, si no las encuentra, directamente en la base de datos.
- **Agendamiento Conversacional**: Mantiene el contexto de la conversación a través de múltiples turnos para recopilar toda la información necesaria (ID de propiedad, fecha y hora) antes de confirmar una visita.
- **Agente Generalista (ReAct)**: Para cualquier pregunta que no se ajuste a las intenciones principales, un agente **ReAct** toma el control para mantener una conversación fluida, utilizando herramientas personalizadas.
- **Memoria Persistente**: Utiliza **Redis** para almacenar el historial de la conversación y el contexto de cada usuario, permitiendo interacciones coherentes a lo largo del tiempo.
- **Arquitectura Modular y Escalable**: Totalmente contenerizado con **Docker Compose**, separando la API, la base de datos, la memoria y la interfaz de usuario.

## 🛠️ Arquitectura del Proyecto

El proyecto está organizado en una estructura de microservicios orquestada por Docker Compose:

- **`api`**: Un servicio **FastAPI** que expone los endpoints para interactuar con el agente.
- **`gradio`**: Una interfaz de usuario web simple y rápida construida con **Gradio** para chatear con el agente.
- **`postgres`**: La base de datos **PostgreSQL** donde se almacenan las propiedades.
- **`redis`**: El broker de memoria **Redis** para gestionar el estado y el historial de las conversaciones.

### 📁 Estructura de Carpetas
Use code with caution.

Markdown
.
├── api/ # Endpoints de FastAPI (main.py)
├── data/ # Archivos de datos (properties.csv)
├── docker/ # Archivos de Docker (Dockerfile, docker-compose.yml)
├── graph/
│ ├── nodes/ # Lógica de cada nodo del grafo (buscar, comparar, etc.)
│ └── property_graph.py # Construcción del grafo con LangGraph
├── scripts/ # Scripts de utilidad (ej: seed_db.py para poblar la DB)
├── tools/ # Herramientas y utilidades (conexión a DB, Redis, herramientas ReAct)
├── app_gradio.py # Script de la interfaz de usuario Gradio
├── config.py # Configuración centralizada
├── requirements.txt # Dependencias de Python para la API
└── README.md # Este archivo

Generated code
## 🚀 Cómo Empezar

Sigue estos pasos para levantar todo el entorno y empezar a interactuar con el agente.

### Prerrequisitos

- **Docker** y **Docker Compose** instalados en tu sistema.
- Una clave de API de **OpenAI** para el funcionamiento de los modelos de lenguaje.

### 1. Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/tu-repositorio.git
cd tu-repositorio
```
Use code with caution.

2. Configurar las Variables de Entorno
Crea un archivo .env en la raíz del proyecto a partir del archivo de ejemplo .env.example (si lo tienes) o créalo desde cero. Debe contener tu clave de API de OpenAI:
Generated env
# .env
OPENAI_API_KEY="sk-..."
Use code with caution.
Env
3. Construir y Ejecutar los Contenedores
Navega a la carpeta docker y usa Docker Compose para construir las imágenes y levantar todos los servicios.

```
Generated bash
cd docker
docker-compose up --build
Use code with caution.
```

La primera vez que se ejecute, esto puede tardar unos minutos mientras se descargan las imágenes base y se instalan las dependencias.
4. Poblar la Base de Datos (Ejecutar solo una vez)
Para que el agente tenga propiedades para buscar, necesitamos cargar los datos desde el archivo data/properties.csv a la base de datos PostgreSQL.
Abre una nueva terminal (sin detener los contenedores) y ejecuta el siguiente comando desde la carpeta docker/:

```Generated bash
docker-compose run --rm api python scripts/seed_db.py
Use code with caution.
```
Bash
Este script creará la tabla properties (si no existe) y la llenará con los datos.

#5. ¡Chatea con el Agente!
Una vez que todos los servicios estén en funcionamiento y la base de datos esté poblada, abre tu navegador web y ve a:
http://localhost:7860
Deberías ver la interfaz de Gradio lista para que empieces a conversar con tu agente inmobiliario.
Ejemplos de Conversación
Búsqueda: busco casa en yerba buena
#Comparación: compara las propiedades 1 y 2
#Agendamiento (multi-turno):
quiero agendar una visita para la id 5
mañana a las 4 de la tarde
Conversación general: ¿cuál es la capital de Francia?
#🔮 Próximos Pasos
Consulta el archivo PROXIMOS_PASOS.md para ver la hoja de ruta detallada con las futuras mejoras planificadas, incluyendo:
Limpieza de contexto post-agendamiento.
Saludos personalizados.
Gestión de "Favoritos".
#Integración con RAG para responder preguntas sobre documentos.
Desarrollado por [Tu Nombre/Tu Equipo]
