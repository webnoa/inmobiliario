
# Real Estate Agent (LangGraph + LangChain)

Sistema modular de agentes IA diseñado para asistir en operaciones inmobiliarias, basado en:
- **LangChain** y **LangGraph**
- **FastAPI** para exponer endpoints
- **PostgreSQL** para almacenamiento de propiedades
- **Redis** para persistencia de conversaciones
- **OpenAI (gpt-4o-mini)** como modelo principal
- Desplegable en Docker + VPS (Contabo)
- Whatsapp + Chatwoot

---

## 📁 Estructura del proyecto

```
real_estate_agent_project/
├── api/
│   └── main.py
├── graph/
│   ├── property_graph.py
│   └── nodes/
│       ├── classifier.py
│       ├── search.py
│       ├── compare.py
│       ├── agendar.py
│       └── react_agent.py
├── scripts/
│   └── load_data.py
├── tools/
│   ├── db.py
│   ├── redis.py
│   ├── intent_embeddings.py
│   ├── react_tools.py
│   └── __init__.py
├── data/
│   └── properties.csv
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🚀 Endpoints disponibles (FastAPI)

- `GET /consulta_graph?q=...&usuario=...` → Ejecuta el flujo LangGraph
- `GET /historial?usuario=...` → Devuelve el historial guardado en Redis

---

## 🧠 Flujo LangGraph

El grafo define un flujo de decisión por intención:

```python
StateGraph(GraphState)
 → clasificar_intencion
     ├── buscar → buscar_propiedades
     ├── comparar → comparar_propiedades
     ├── agendar → agendar_visita
     └── otro → react_agent
```

---

## 🔐 Variables de entorno (.env)

Ejemplo (`.env.example`):

```env
OPENAI_API_KEY=sk-xxx
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=properties
REDIS_HOST=redis
REDIS_PORT=6379
```

---

## ⚙️ Setup (Modo Docker)

1. Copiar `.env.example` → `.env`
2. Levantar servicios:
```bash
docker compose up --build
```
3. Cargar propiedades:
```bash
docker compose exec api bash
python scripts/load_data.py
```

---

## 🔍 Clasificador con semántica

- Usa keywords, LLM (gpt-4o-mini), y embeddings + FAISS para mayor precisión.
- Historial guardado con pregunta, intención, respuesta y timestamp por usuario.

---

## 📌 Próximos pasos

- Mejora del agente `agendar_visita` (validación + agenda persistente)
- Continuación de sesiones y recuperación de contexto
- Conexión con canal WhatsApp o interfaz web
