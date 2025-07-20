
import pytest
from graph.property_graph import build_graph
from tools import redis as redis_tools

@pytest.fixture(autouse=True)
def limpiar_contexto(monkeypatch):
    # mock redis persistencia en memoria
    store = {}
    def mock_guardar_contexto(usuario, campo, valor):
        store.setdefault(usuario, {})[campo] = valor
    def mock_recuperar_contexto(usuario, campo):
        return store.get(usuario, {}).get(campo)
    def mock_guardar_en_historial(usuario, pregunta, intencion, respuesta):
        pass
    def mock_recuperar_historial(usuario, filtro_intencion=None):
        return []
    monkeypatch.setattr(redis_tools, "guardar_contexto", mock_guardar_contexto)
    monkeypatch.setattr(redis_tools, "recuperar_contexto", mock_recuperar_contexto)
    monkeypatch.setattr(redis_tools, "guardar_en_historial", mock_guardar_en_historial)
    monkeypatch.setattr(redis_tools, "recuperar_historial", mock_recuperar_historial)
    yield

def test_flujo_buscar_comparar_agendar(monkeypatch):
    # mock DB
    from tools import db as db_tools
    dummy_props = [
        {"id": 1, "title": "Casa con patio", "ubicacion": "San Miguel", "precio": 75000, "tipo": "Casa", "ambientes": 3},
        {"id": 2, "title": "Depto céntrico", "ubicacion": "Centro", "precio": 58000, "tipo": "Departamento", "ambientes": 2},
    ]
    monkeypatch.setattr(db_tools, "buscar_propiedades", lambda txt: dummy_props)
    monkeypatch.setattr(db_tools, "obtener_propiedades_por_ids", lambda ids: [p for p in dummy_props if p["id"] in ids])

    grafo = build_graph()
    usuario = "jose"
    state = {"usuario": usuario, "pregunta": "Busco una casa con patio", "intencion": "", "respuesta": ""}
    state = grafo.invoke(state)
    assert "Casa con patio" in state["respuesta"]

    state = {"usuario": usuario, "pregunta": "¿Cuál me conviene más?", "intencion": "", "respuesta": ""}
    state = grafo.invoke(state)
    assert "Propiedad" in state["respuesta"] and "vs" in state["respuesta"]

    state = {"usuario": usuario, "pregunta": "Quiero agendar para mañana a las 18hs", "intencion": "", "respuesta": ""}
    state = grafo.invoke(state)
    assert "Visita agendada" in state["respuesta"] or "Necesito" in state["respuesta"]
