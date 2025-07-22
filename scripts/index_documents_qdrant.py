# Ruta: /REAL_ESTATE_AGENT/scripts/index_documents_qdrant.py

import os
import sys
from langchain_qdrant import Qdrant
from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from config import OPENAI_API_KEY

# Añadir la raíz del proyecto al path para importaciones
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = 6333
COLLECTION_NAME = "propiedades_detalles"
DOCUMENTS_PATH = "data/property_docs"

def main():
    """
    Script para leer documentos, dividirlos, crear embeddings y guardarlos
    en la base de datos vectorial Qdrant usando la integración de LangChain.
    """
    print("🚀 Iniciando proceso de indexación de documentos para RAG con Qdrant...")

    # 0. Crear la carpeta de documentos si no existe y añadir un ejemplo
    if not os.path.exists(DOCUMENTS_PATH):
        os.makedirs(DOCUMENTS_PATH)
        print(f"Creada la carpeta '{DOCUMENTS_PATH}'. Por favor, añade tus PDFs o TXTs allí.")
        with open(os.path.join(DOCUMENTS_PATH, "propiedad_2.txt"), "w") as f:
            f.write("Detalles de la Propiedad ID 2: La casa en Yerba Buena tiene expensas de $15,000. El reglamento no permite mascotas de gran tamaño, solo una mascota pequeña por apartamento.")
        print("Creado un archivo de ejemplo: 'propiedad_2.txt'")

    # 1. Cargar los documentos
    loader = DirectoryLoader(DOCUMENTS_PATH, glob="**/*.txt", show_progress=True)
    docs = loader.load()
    if not docs:
        print("No se encontraron documentos para indexar. Proceso finalizado.")
        return
    print(f"Cargados {len(docs)} documentos desde '{DOCUMENTS_PATH}'.")

    # 2. Dividir los documentos en fragmentos (chunks)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    splits = text_splitter.split_documents(docs)
    print(f"Documentos divididos en {len(splits)} fragmentos.")

    # 3. Inicializar el modelo de embeddings
    embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY, model="text-embedding-3-small")
    print("Modelo de embeddings inicializado.")

    # 4. Indexar los fragmentos en Qdrant
    # LangChain se encarga de la conexión, creación de la colección y la indexación.
    # Si la colección ya existe, añadirá los nuevos documentos.
    print(f"Indexando documentos en la colección '{COLLECTION_NAME}' de Qdrant...")
    
    try:
        qdrant = Qdrant.from_documents(
            splits,
            embeddings,
            host=QDRANT_HOST,
            port=QDRANT_PORT,
            collection_name=COLLECTION_NAME,
        )
        print(f"✅ ¡Indexación completada! {len(splits)} fragmentos guardados en Qdrant.")
        print(f"Vector store info: {qdrant}")

    except Exception as e:
        print(f"🚨 Error durante la indexación en Qdrant: {e}")
        print("Asegúrate de que el contenedor de Qdrant esté en ejecución y accesible.")

if __name__ == "__main__":
    main()