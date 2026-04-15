from fastapi import FastAPI, UploadFile, File
import PyPDF2
from io import BytesIO

app = FastAPI()

@app.post("/analizar")
def analizar(file: UploadFile = File(...)):
    contenido = file.file.read()

    pdf_stream = io.BytesIO(contenido)

    reader = PyPDF2.PdfReader(pdf_stream)
    texto_pdf = ""

    for page in reader.pages:
        texto_pdf += page.extract_text() or ""

    resultado = analizar_contrato(texto_pdf)

    return {
        "mensaje": "PDF recibido correctamente",
        "resultado": resultado
    }