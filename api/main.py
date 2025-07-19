from fastapi import FastAPI, Query
from graph.property_graph import build_graph

app = FastAPI()

@app.get("/consulta_graph")
def consulta_por_grafo(q: str, usuario: str = "anonimo"):
    graph = build_graph()
    output = graph.invoke({"pregunta": q, "usuario": usuario})
    return {"respuesta": output["respuesta"]}

@app.get("/historial")
def ver_historial(usuario: str = "anonimo"):
    from tools.redis import recuperar_historial
    historial = recuperar_historial(usuario)
    return {"historial": historial}