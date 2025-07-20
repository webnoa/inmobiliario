
# tests/test_agendar.py

import pytest
from graph.nodes.agendar import agendar_visita_node

class MockRedis:
    def __init__(self):
        self.store = {}

    def set(self, key, value):
        self.store[key] = value

    def get(self, key):
        return self.store.get(key)

@pytest.fixture
def mock_redis(monkeypatch):
    from tools import redis as redis_tools
    mock_instance = MockRedis()

    # Mockear get_redis_connection para que devuelva la clase mock
    monkeypatch.setattr(redis_tools, "get_redis_connection", lambda: mock_instance)

    return mock_instance

def test_agendar_visita_valida(mock_redis):
    state = {
        "usuario": "jose",
        "input": {
            "propiedad_id": 23,
            "fecha": "2099-07-21",
            "hora": "15:30"
        }
    }

    resultado = agendar_visita_node(state)

    assert "✅" in resultado["output"]
    assert resultado["output"].startswith("✅ Visita agendada")
    assert "agenda_visitas:2099-07-21 15:30" in mock_redis.store
