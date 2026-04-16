from django import forms
from .models import Contrato

class ContratoForm(forms.ModelForm):
    class Meta:
        model = Contrato
        fields = ["nombre", "cliente", "tipo", "archivo_pdf"]