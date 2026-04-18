import json
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()

class AgenteIA:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash", # Versión más estable
            temperature=0,
            max_output_tokens=1000,
        )

    def analizar(self, texto: str, prompt_especifico: str):
        prompt_sistema = f"""
            Eres un experto en derecho contractual. Analiza el contrato proporcionado siguiendo las instrucciones específicas.
            
            INSTRUCCIONES ESPECÍFICAS:
            {prompt_especifico}

            ADEMÁS, debes extraer los siguientes datos clave:
            - Nombres de las partes.
            - DNIs o pasaportes mencionados.
            - Fechas importantes (inicio, fin, firma).
            - Importes económicos (fianzas, mensualidades, multas).

            DEBES RESPONDER ÚNICAMENTE EN FORMATO JSON VÁLIDO.
            Formato de respuesta:
            {{
                "puntos_clave": ["lista", "de", "puntos"],
                "banderas_rojas": ["lista", "de", "cláusulas", "peligrosas"],
                "riesgo_total": "Bajo" | "Medio" | "Crítico",
                "entidades": {{
                    "nombres": ["nombre1", "nombre2"],
                    "dni": ["DNI1"],
                    "fechas": ["fecha1"],
                    "importes": ["importe1"]
                }}
            }}
        """

        prompt_usuario = f"Contrato a analizar:\n{texto}"
        
        try:
            response = self.llm.invoke([
                ("system", prompt_sistema),
                ("user", prompt_usuario)
            ])
            
            contenido = response.content.strip()
            
            # Limpieza básica para asegurar JSON válido
            inicio = contenido.find("{")
            fin = contenido.rfind("}") + 1
            json_str = contenido[inicio:fin]
            
            return json.loads(json_str)
            
        except Exception as e:
            return {
                "puntos_clave": ["Error al procesar"],
                "banderas_rojas": [f"Error de conexión: {str(e)}"],
                "riesgo_total": "Crítico"
            }

# Instancia única para ser reutilizada
agente = AgenteIA()