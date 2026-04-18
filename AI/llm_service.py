import json
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

# Cargamos las variables del .env
load_dotenv()

# Clase para interactuar con la IA de Google
class AgenteIA:
    def __init__(self):
        # Configuracion del modelo Gemini
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash", # Versión más estable
            temperature=0,
            max_output_tokens=1000,
        )

    # Funcion principal de analisis
    def analizar(self, texto: str, prompt_especifico: str):
        prompt_sistema = f"""
            Eres un experto en derecho contractual. Analiza el contrato siguiendo estas instrucciones.
            
            INSTRUCCIONES:
            {prompt_especifico}

            EXTRAE TAMBIEN:
            - Nombres de las partes.
            - DNIs o identificaciones.
            - Fechas clave.
            - Importes economicos.

            RESPONDE SOLO EN JSON:
            {{
                "puntos_clave": ["..."],
                "banderas_rojas": ["..."],
                "riesgo_total": "Bajo" | "Medio" | "Critico",
                "entidades": {{
                    "nombres": [],
                    "dni": [],
                    "fechas": [],
                    "importes": []
                }}
            }}
        """

        prompt_usuario = f"Contrato:\n{texto}"
        
        try:
            # Llamada al LLM
            response = self.llm.invoke([
                ("system", prompt_sistema),
                ("user", prompt_usuario)
            ])
            
            contenido = response.content.strip()
            
            # Limpiamos el texto para sacar solo el JSON
            inicio = contenido.find("{")
            fin = contenido.rfind("}") + 1
            json_str = contenido[inicio:fin]
            
            return json.loads(json_str)
            
        except Exception as e:
            # En caso de error devolvemos un JSON basico
            return {
                "puntos_clave": ["Error"],
                "banderas_rojas": [f"Fallo de conexion: {str(e)}"],
                "riesgo_total": "Critico",
                "entidades": {"nombres": [], "dni": [], "fechas": [], "importes": []}
            }

# Instancia global del agente
agente = AgenteIA()