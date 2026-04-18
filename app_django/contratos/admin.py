from django.contrib import admin
from django.utils import timezone
from .models import Contrato
import json

# Registro del modelo de contratos en el admin
@admin.register(Contrato)
class ContratoAdmin(admin.ModelAdmin):
    # Campos que se ven en la lista
    list_display = ('nombre_orig_pdf', 'cliente', 'tipo', 'fecha_subida')
    # Filtros laterales
    list_filter = ('tipo', 'fecha_subida')
    # Buscador por nombre y cliente
    search_fields = ('nombre_orig_pdf', 'cliente')

    # Vista principal con estadísticas
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        
        # Fecha de hoy
        hoy = timezone.now().date()
        
        # Contratos analizados hoy
        extra_context['total_hoy'] = Contrato.objects.filter(fecha_subida__date=hoy).count()
        
        # Cálculo de trampas más comunes
        alertas = []
        contratos = Contrato.objects.all()
        for c in contratos:
            res = c.get_resultado()
            if 'banderas_rojas' in res:
                alertas.extend(res['banderas_rojas'])
        
        # Sacamos las 3 más frecuentes
        from collections import Counter
        top_alertas = Counter(alertas).most_common(3)
        extra_context['top_alertas'] = top_alertas
        
        return super().changelist_view(request, extra_context=extra_context)
