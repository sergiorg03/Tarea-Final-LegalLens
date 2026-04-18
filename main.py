from fastapi import FastAPI, UploadFile, File, Form
import fitz  # PyMuPDF
from AI.llm_service import agente
from AI.contratos import ContratoFactory
import uvicorn

# Inicializamos la aplicacion FastAPI
app = FastAPI()

# Endpoint para analizar el contrato
@app.post("/analizar")
async def analizar(
    file: UploadFile = File(...), 
    tipo: str = Form(...), 
    cliente: str = Form("Desconocido")
):
    # Leemos los bytes del PDF
    contenido = await file.read()
    
    # Extraemos el texto usando PyMuPDF
    texto_pdf = ""
    try:
        with fitz.open(stream=contenido, filetype="pdf") as doc:
            for page in doc:
                texto_pdf += page.get_text()
    except Exception as e:
        return {"error": f"Error al leer el PDF: {str(e)}"}

    # Procesamos segun el tipo de contrato (POO)
    try:
        # Usamos la Factory para crear el contrato adecuado (Alquiler o NDA)
        instancia_contrato = ContratoFactory.crear_contrato(tipo, texto_pdf, cliente)
        
        # Ejecutamos la auditoria con la IA
        resultado = instancia_contrato.ejecutar_auditoria(agente)
        
        return resultado
    except ValueError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": f"Error en el procesamiento: {str(e)}"}

# Arrancamos el servidor si se ejecuta directo
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)