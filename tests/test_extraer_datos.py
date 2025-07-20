from graph.nodes.extraer_datos_agenda import extraer_datos_agenda_node
from tools import redis as redis_tools

def test_extraccion_semantica(monkeypatch):
    mock_store = {}

    monkeypatch.setattr(redis_tools, "guardar_contexto", lambda usuario, campo, valor: mock_store.update({campo: valor}))

    state = {
        "pregunta": "Quiero visitar la casa 42 mañana a las 19hs",
        "usuario": "jose",
        "intencion": "",
        "respuesta": ""
    }

    extraer_datos_agenda_node(state)
    datos = mock_store.get("datos_visita")
    assert datos
    assert "fecha" in datos
    assert "hora" in datos
    assert datos["propiedad_id"] == 42
