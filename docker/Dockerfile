# Ruta: /REAL_ESTATE_AGENT/docker/Dockerfile

# Usamos una imagen base de Python 3.11 slim para un tamaño reducido
FROM python:3.11-slim

# --- PASO CLAVE: Instalar dependencias del sistema ---
# Actualizamos los repositorios e instalamos 'graphviz', que es necesario
# para que la librería de Python 'pygraphviz' funcione correctamente.
RUN apt-get update && apt-get install -y --no-install-recommends graphviz && rm -rf /var/lib/apt/lists/*

# Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos solo el archivo de requerimientos primero para aprovechar el cache de Docker
COPY requirements.txt .

# Instalamos todas las librerías de Python, incluyendo pygraphviz
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del código de la aplicación
COPY . .

# El comando por defecto para iniciar la API (no se usa al ejecutar el script de visualización)
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]