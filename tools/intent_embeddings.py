from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")

intenciones = ["buscar", "comparar", "agendar", "otro"]
docs = [f"intención: {i}" for i in intenciones]
metadatas = [{"intencion": i} for i in intenciones]
vectorstore = FAISS.from_texts(docs, embedding_model, metadatas=metadatas)

def clasificar_por_semantica(pregunta: str) -> str:
    resultados = vectorstore.similarity_search(pregunta, k=1)
    return resultados[0].metadata["intencion"]