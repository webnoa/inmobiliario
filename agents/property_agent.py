from langchain.agents import initialize_agent, AgentType
from langchain_community.chat_models import ChatOpenAI
from tools.property_search import buscar_propiedades

# Instancia del modelo de lenguaje
llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")

# Lista de herramientas disponibles
tools = [buscar_propiedades]

# Inicialización del agente
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)
