from fastapi import FastAPI, UploadFile, File, Form
import fitz  # PyMuPDF
from io import BytesIO
from AI.llm_service import agente
from AI.contratos import ContratoFactory
import uvicorn

app = FastAPI()

@app.post("/analizar")
async def analizar(
    file: UploadFile = File(...), 
    tipo: str = Form(...), 
    cliente: str = Form("Desconocido")
):
    # Leer el contenido del archivo
    contenido = await file.read()
    
    # Extraer texto usando PyMuPDF
    texto_pdf = ""
    try:
        with fitz.open(stream=contenido, filetype="pdf") as doc:
            for page in doc:
                texto_pdf += page.get_text()
    except Exception as e:
        return {"error": f"Error al leer el PDF: {str(e)}"}

    
    try:
        # Obtiene el contrato correcto (Alquiler o NDA)
        instancia_contrato = ContratoFactory.crear_contrato(tipo, texto_pdf, cliente)
        
        # Ejecuta la auditoría usando el agente IA
        resultado = instancia_contrato.ejecutar_auditoria(agente)
        
        return resultado
    except ValueError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": f"Error en el procesamiento: {str(e)}"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)