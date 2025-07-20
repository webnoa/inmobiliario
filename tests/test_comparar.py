# tests/test_comparar.py

import pytest
import tools.redis
import tools.db

def test_comparar_con_contexto(monkeypatch):
    mock_contexto = [
        {"id": 1, "tipo": "Casa", "ambientes": 4},
        {"id": 2, "tipo": "Departamento", "ambientes": 3}
    ]

    monkeypatch.setattr(tools.redis, "recuperar_contexto", lambda usuario, campo: mock_contexto)

    def mock_obtener(ids):
        return [p for p in mock_contexto if p["id"] in ids]

    monkeypatch.setattr(tools.db, "obtener_propiedades_por_ids", mock_obtener)

    # Importar después de los patches
    from graph.nodes.compare import comparar_propiedades_node

    state = {
        "usuario": "jose",
        "input": {}
    }

    resultado = comparar_propiedades_node(state)

    assert "Propiedad 1" in resultado["respuesta"]
    assert "vs Propiedad 2" in resultado["respuesta"]