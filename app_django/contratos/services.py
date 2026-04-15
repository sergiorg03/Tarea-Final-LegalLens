import requests
import json
import os

API_URL = os.getenv("API_URL", "http://localhost:8001/analizar")

def llamar_api_ia(pdf_file):
    try:
        response = requests.post(
            API_URL,
            files={"file": pdf_file},
            timeout=30
        )

        print("STATUS:", response.status_code)
        print("RESPUESTA:", response.text)

        response.raise_for_status()

        return response.json()

    except Exception as e:
        print("ERROR IA:", e)
        return {
            "abusivo": False,
            "clausulas": [],
            "motivo": "Error en la comunicación con la IA"
        }


def guardar_resultado_ia(contrato, resultado):
    contrato.resultado_ia = json.dumps(resultado)
    contrato.save()


def obtener_resultado_ia(contrato):
    try:
        return json.loads(contrato.resultado_ia)
    except:
        return {
            "abusivo": False,
            "clausulas": [],
            "motivo": "Error al procesar la respuesta"
        }