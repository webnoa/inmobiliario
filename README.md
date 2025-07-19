# 🏡 Agente Inmobiliario Autónomo

Este proyecto implementa un agente de IA modular para consultas inmobiliarias (búsqueda, comparación y agenda de visitas), utilizando **LangGraph**, **LangChain**, **PostgreSQL**, **Redis** y **FastAPI**.

---

## ⚙️ Tecnologías

- [LangGraph](https://langchain-ai.github.io/langgraph/)
- [LangChain](https://www.langchain.com/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [PostgreSQL](https://www.postgresql.org/)
- [Redis](https://redis.io/)
- [Docker Compose](https://docs.docker.com/compose/)

---

## 🧠 Capacidades del agente

- Clasificación semántica de intención (buscar, comparar, agendar, otro)
- Persistencia del historial por usuario (Redis)
- Consulta y carga de propiedades (PostgreSQL)
- Nodo de agente ReAct para consultas generales
- Registro y validación de visitas simuladas
- Registro de historial detallado: pregunta, intención, respuesta, timestamp

---

## 🚀 Estructura del proyecto

 │    agents/property_agent.py                                                                       │
 │    api/main.py                                                                                    │
 │    config.py                                                                                      │
 │    docker/Dockerfile                                                                              │
 │    docker/docker-compose.yml                                                                      │
 │    graph/nodes/agenda.py                                                                          │
 │    graph/nodes/agendar.py                                                                         │
 │    graph/nodes/classifier.py                                                                      │
 │    graph/nodes/compare.py                                                                         │
 │    graph/nodes/final.py                                                                           │
 │    graph/nodes/historial.py                                                                       │
 │    graph/nodes/react_agent.py                                                                     │
 │    graph/nodes/search.py                                                                          │
 │    graph/property_graph.py                                                                        │
 │    requirements.txt                                                                               │
 │    .env                                                                               │
 │    scripts/load_data.py                                                                           │
 │    tools/db.py                                                                                    │
 │    tools/intent_embeddings.py                                                                     │
 │    tools/property_search.py                                                                       │
 │    tools/react_tools.py                                                                           │
 │    tools/redis.py

# Resumen del Proyecto

## Estado actual
- Clasificador con embeddings y fallback a LLM
- Historial en Redis por usuario
- Nodo de agenda con validación
- Ramas: buscar, comparar, agendar, otro (ReAct)

## Próximos pasos
- Sesiones
- Interfaz Web y WhatsApp
- Base de propiedades más robusta
- Testing y monitoreo
