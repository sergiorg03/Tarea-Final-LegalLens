from django.db import models
import uuid

# Create your models here.
def ruta_pdf(instance, filename):
    extension = filename.split(".")[-1]
    return f"archivos_pdf/archivo_{uuid.uuid4().hex}.{extension}"


class Contrato(models.Model):
    nombre = models.CharField(max_length=255)
    fecha_subida = models.DateTimeField(auto_now_add=True)
    resultado_ia = models.TextField()

    archivo_pdf = models.FileField(upload_to=ruta_pdf)
    nombre_orig_pdf = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.nombre_orig_pdf
