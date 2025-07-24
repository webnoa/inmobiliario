# Ruta: /REAL_ESTATE_AGENT/visualize_graph.py

# Este script es para generar una representación visual del grafo de LangGraph.
# Se debe ejecutar de forma independiente, no es parte de la API.

from graph.property_graph import build_graph
import os

def generar_visualizacion_grafo():
    """
    Construye el grafo y genera una imagen PNG que lo representa.
    """
    print("Construyendo el grafo para la visualización...")
    # Construimos la instancia del grafo, igual que en la API
    graph = build_graph()
    
    # Nombre del archivo de salida
    output_file = "graph_visualization.png"
    
    print(f"Generando la imagen del grafo en '{output_file}'...")
    
    try:
        # get_graph() nos da acceso a la estructura interna para poder dibujarla
        # draw_mermaid_png() genera la imagen. Requiere dependencias adicionales.
        png_bytes = graph.get_graph().draw_mermaid_png()
        
        # Guardamos los bytes en un archivo
        with open(output_file, "wb") as f:
            f.write(png_bytes)
            
        print(f"\n¡Éxito! El grafo se ha guardado en {os.path.abspath(output_file)}")
        print("Puedes abrir este archivo para ver la estructura de tu agente.")
        
    except Exception as e:
        print(f"\n🚨 ¡Error al generar la imagen del grafo! 🚨\nEs muy probable que falten dependencias para la visualización. Lee las instrucciones sobre cómo instalar 'pygraphviz' y 'Graphviz'.\n\nError original: {e}")

if __name__ == "__main__":
    generar_visualizacion_grafo()