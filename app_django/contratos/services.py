import requests
import json
import os

# URL de la API de IA (se saca del entorno o usa localhost)
API_URL = os.getenv("API_URL", "http://localhost:8001/analizar")

# Función para enviar el PDF al motor de FastAPI
def llamar_api_ia(contrato):
    try:
        with contrato.archivo_pdf.open("rb") as pdf:
            response = requests.post(
                API_URL,
                files={"file": pdf},
                data={
                    "tipo": contrato.tipo,
                    "cliente": contrato.cliente
                },
                timeout=60
            )

        response.raise_for_status()
        return response.json()

    except Exception as e:
        print("ERROR IA:", e)
        return {
            "riesgo_total": "Bajo",
            "banderas_rojas": [],
            "puntos_clave": ["Error en la comunicación con la IA"]
        }

# Guarda el JSON de la IA en la base de datos
def guardar_resultado_ia(contrato, resultado):
    contrato.resultado_ia = json.dumps(resultado)
    contrato.save()

# Recupera y parsea el JSON guardado
def obtener_resultado_ia(contrato):
    try:
        return json.loads(contrato.resultado_ia)
    except:
        return {
            "riesgo_total": "Bajo",
            "banderas_rojas": [],
            "puntos_clave": ["Error al procesar la respuesta"]
        }