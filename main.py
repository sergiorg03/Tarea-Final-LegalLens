from fastapi import FastAPI, UploadFile, File

app = FastAPI()

@app.post("/analizar")
async def analizar_pdf(file: UploadFile = File(...)):
    contenido = await file.read()
    return {'mensaje': "PDF recibido correctamente", 'resultado':"Hola"} # TODO: Cambiar el resultado devuelto