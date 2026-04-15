from django.urls import path
from . import views

urlpatterns = [
    path("", views.subir_contrato, name="subir_contrato"),
    path("contrato/<int:pk>/", views.info_contrato, name="info_contrato"),
]