import logging

from django.http import FileResponse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import ContratoForm
from .models import Contrato
from .services import llamar_api_ia, guardar_resultado_ia, obtener_resultado_ia

logger = logging.getLogger(__name__)

def subir_contrato(request):
    """
        Función que sube un contrato.
        Parámetros:
            - request: objeto request de Django
        Retorna:
            - render: template subir_contrato.html con el formulario de subida de contrato
    """
    if request.method == "POST":
        form = ContratoForm(request.POST, request.FILES)

        if form.is_valid():
            contrato = form.save()

            contrato.nombre_orig_pdf = request.FILES["archivo_pdf"].name
            contrato.save()

            with contrato.archivo_pdf.open("rb") as pdf:
                resultado = llamar_api_ia(pdf)

            guardar_resultado_ia(contrato, resultado)

            return redirect("info_contrato", pk=contrato.pk)

    else:
        form = ContratoForm()

    return render(request, "contratos/subir_contrato.html", {"form": form})

def info_contrato(request, pk: int):
    """
        Función que muestra la información del contrato seleccionado.
        Parámetros:
            - request: objeto request de Django
            - pk: id del contrato a mostrar
        Retorna:
            - render: template info_contrato.html con el contrato seleccionado
    """
    contrato = get_object_or_404(Contrato, pk=pk)

    resultado = obtener_resultado_ia(contrato)

    return render(request, "contratos/info_contrato.html", {
        "contrato": contrato,
        "motivo": resultado.get("motivo"),
        "clausulas_abusivas": resultado.get("clausulas"),
        "abusivo": resultado.get("abusivo")
    })

def descargar_pdf(request, pk):
    """
        Función que descarga el PDF del contrato seleccionado.
        Parámetros:
            - request: objeto request de Django
            - pk: id del contrato a descargar
        Retorna:
            - FileResponse: archivo PDF del contrato
    """
    contrato = Contrato.objects.get(pk=pk)

    return FileResponse(
        contrato.archivo_pdf.open("rb"),
        as_attachment=True,
        filename=contrato.nombre_orig_pdf
    )