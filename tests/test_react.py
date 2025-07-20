def test_saludo_personalizado_directo():
    from graph.nodes.react_agent import react_agent_node
    state = {
        "pregunta": "Hola, me llamo José",
        "usuario": "jose"
    }
    result = react_agent_node(state)
    print("💬 Respuesta del agente:", result["respuesta"])
    assert "Hola José" in result["respuesta"]