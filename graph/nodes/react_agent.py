from typing import TypedDict
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain.agents import AgentExecutor
from tools.react_tools import tools  # Asegúrate que este archivo exista

class GraphState(TypedDict):
    pregunta: str
    intencion: str
    respuesta: str
    usuario: str

llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")

# Crea el agente ReAct prearmado con el prompt correcto
agent = create_react_agent(llm, tools)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

def react_agent_node(state: GraphState) -> GraphState:
    respuesta = agent_executor.invoke({"input": state["pregunta"]})["output"]
    return {**state, "respuesta": respuesta}

