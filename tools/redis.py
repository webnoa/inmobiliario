import json
from datetime import datetime
import redis
from config import REDIS

def get_redis_connection():
    return redis.Redis(host=REDIS["host"], port=REDIS["port"], decode_responses=True)

def guardar_en_historial(usuario: str, pregunta: str, intencion: str, respuesta: str):
    r = get_redis_connection()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entrada = {
        "timestamp": timestamp,
        "pregunta": pregunta,
        "intencion": intencion,
        "respuesta": respuesta
    }
    r.lpush(f"historial:{usuario}", json.dumps(entrada))

def recuperar_historial(usuario: str, filtro_intencion: str = None):
    r = get_redis_connection()
    claves = r.lrange(f"historial:{usuario}", 0, 9)
    historial = []
    for k in claves:
        entrada = json.loads(k)
        if not filtro_intencion or entrada["intencion"] == filtro_intencion:
            historial.append(entrada)
    return historial