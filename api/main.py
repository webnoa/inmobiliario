from fastapi import FastAPI, Query
from graph.property_graph import build_graph
from tools.redis import recuperar_historial, recuperar_contexto


app = FastAPI()

@app.get("/consulta_graph")
def consulta_por_grafo(q: str, usuario: str = "anonimo"):
    graph = build_graph()
    output = graph.invoke({"pregunta": q, "usuario": usuario, "intencion": "", "respuesta": ""})
    return {"respuesta": output["respuesta"]}

@app.get("/historial")
def ver_historial(usuario: str = "anonimo"):
    historial = recuperar_historial(usuario)
    return {"historial": historial}

@app.get("/ver_contexto")
def ver_contexto(usuario: str = "anonimo", campo: str = "datos_visita"):
    contexto = recuperar_contexto(usuario, campo)
    return {"usuario": usuario, "campo": campo, "contexto": contexto}

@app.get("/flujo_demo_completo")
def flujo_demo_completo(usuario: str = "jose"):
    grafo = build_graph()
    interacciones = [
        "Busco una casa con patio",
        "¿Cuál me conviene más?",
        "Quiero agendar para mañana a las 18hs",
    ]
    resultados = []
    state = {"usuario": usuario, "intencion": "", "respuesta": ""}
    for p in interacciones:
        state = {**state, "pregunta": p, "intencion": "", "respuesta": ""}
        state = grafo.invoke(state)
        resultados.append(state)
    return {"flujo": resultados}