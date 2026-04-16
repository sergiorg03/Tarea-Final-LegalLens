from fastapi import FastAPI, UploadFile, File
import PyPDF2
from io import BytesIO
from AI.llm_service import analizar_contrato

app = FastAPI()

@app.post("/analizar")
def analizar(file: UploadFile = File(...)):
    contenido = file.file.read()

    pdf_stream = BytesIO(contenido)

    reader = PyPDF2.PdfReader(pdf_stream)
    texto_pdf = ""

    for page in reader.pages:
        texto_pdf += page.extract_text() or ""

    resultado = analizar_contrato(texto_pdf)

    return resultado