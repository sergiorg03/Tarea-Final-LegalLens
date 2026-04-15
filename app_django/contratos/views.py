from django.shortcuts import render, redirect, get_object_or_404
from django.http import FileResponse
from .forms import ContratoForm
from .models import Contrato
import requests

# Create your views here.

def subir_contrato(request):
    if request.method == "POST":
        form = ContratoForm(request.POST, request.FILES)

        if form.is_valid():
            contrato = form.save() # guardamos el contrato

            # Guardamos el nombre original
            contrato.nombre_original = request.FILES["archivo_pdf"].name
            contrato.save()

            # conectamos con FastAPI 
            with contrato.archivo_pdf.open("rb") as pdf:
                response = requests.post(
                    "http://localhost:8001/analizar",
                    files={"file": pdf}
                )

            # Guardamos el resultado
            resultado = response.json()

            #print(f"\n\nEste es el resultado: {resultado}\n\n")

            contrato.resultado_ia = resultado["resultado"]
            contrato.save()

            pk = contrato.pk

            return redirect("info_contrato", pk=pk)

    else:
        form = ContratoForm()

    return render(request, "contratos/subir_contrato.html", {"form": form})

def info_contrato(request, pk: int):
    contrato = get_object_or_404(Contrato, pk=pk)
    return render(request, "contratos/info_contrato.html", {"contrato": contrato})

def descargar_pdf(request, pk):
    contrato = Contrato.objects.get(pk=pk)

    return FileResponse(
        contrato.archivo_pdf.open("rb"),
        as_attachment=True,
        filename=contrato.nombre_original
    )

def ver_contratos():
    pass