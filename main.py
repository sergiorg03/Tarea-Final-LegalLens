from fastapi import FastAPI, UploadFile, File

app = FastAPI()

@app.post("/analizar")
def analizar(file: UploadFile = File(...)):
    contenido = file.file.read()

    with open("archivo.pdf", "wb") as f:
        f.write(contenido)

    texto_pdf = ''
    with open("archivo_temp.pdf", "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            texto_pdf += page.extract_text()
    

    resultado = analizar_contrato(texto_pdf)

    # Devolvemos el resultado de la IA
    return {'mensaje': "PDF recibido correctamente", 'resultado': resultado.content}