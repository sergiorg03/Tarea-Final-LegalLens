import json
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

# Inicializar modelo
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    temperature=0,
    max_output_tokens=500,
)

def analizar_contrato(texto):
    prompt = f"""
        Eres un experto en derecho contractual y protección del consumidor.

        Analiza el siguiente contrato y determina si contiene cláusulas abusivas.

        Debes responder SIEMPRE en formato JSON válido, sin añadir texto fuera del JSON.

        Formato exacto:

        {{
        "abusivo": true/false,
        "clausulas": ["lista de cláusulas abusivas detectadas"],
        "motivo": "explicación breve"
        }}

        Reglas:
        - Si hay cualquier indicio de abuso → abusivo = true
        - Si no hay evidencia clara → abusivo = false
        - Máximo 2-3 líneas en el motivo
        - No inventes información
        - No escribas nada fuera del JSON

        Contrato:
        {texto}
    """

    response = llm.invoke(prompt)
    texto_respuesta = response.content.strip()

    # Limpiamos la respuesta de la IA por si las moscas
    inicio = texto_respuesta.find("{")
    fin = texto_respuesta.rfind("}") + 1

    json_limpio = texto_respuesta[inicio:fin]

    # Lo convertimos a diccionario para evitar errores en Django
    try:
        resultado = json.loads(json_limpio)
    except:
        resultado = {
            "abusivo": False,
            "clausulas": [],
            "motivo": "Error al procesar la respuesta del modelo"
        }

    return resultado # Devolvemos el resultado como un diccionario