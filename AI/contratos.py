from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import List

# 1. El "molde" para los datos que devuelve la IA
class EntidadesExtraidas(BaseModel):
    nombres: List[str]
    dni: List[str]
    fechas: List[str]
    importes: List[str]

class AnalisisResultado(BaseModel):
    puntos_clave: List[str]
    banderas_rojas: List[str]
    riesgo_total: str  # "Bajo", "Medio", "Crítico"
    entidades: EntidadesExtraidas

# 2. La Clase Abstracta
class Contrato(ABC):
    def __init__(self, texto: str, cliente: str):
        self.texto = texto
        self.cliente = cliente

    @abstractmethod
    def obtener_prompt_especifico(self) -> str:
        """Cada subclase dirá qué trampas buscar según su tipo."""
        pass

    def ejecutar_auditoria(self, agente_ia) -> dict:
        """
        Método Plantilla (Template Method): Define el flujo de la auditoría.
        Es común para todos los contratos, pero usa prompts específicos de los hijos.
        """
        prompt = self.obtener_prompt_especifico()
        return agente_ia.analizar(self.texto, prompt)

# 3. Implementaciones concretas
class ContratoAlquiler(Contrato):
    def obtener_prompt_especifico(self) -> str:
        return """
        Busca específicamente:
        1. Si la fianza exigida supera el límite legal (1 mes para vivienda).
        2. Si el contrato obliga al inquilino a pagar reparaciones estructurales o de mantenimiento general (Art. 21 LAU).
        3. Cláusulas de acceso ilimitado del casero a la vivienda.
        """

class ContratoNDA(Contrato):
    def obtener_prompt_especifico(self) -> str:
        return """
        Busca específicamente:
        1. Cláusulas de duración infinita o perpetua de la confidencialidad.
        2. Multas desproporcionadas por filtraciones accidentales (ej: superiores a 100.000€).
        3. Definiciones de 'Información Confidencial' demasiado amplias que incluyan conocimientos previos del trabajador.
        """

# Instancia la clase correcta
class ContratoFactory:
    @staticmethod
    def crear_contrato(tipo: str, texto: str, cliente: str) -> Contrato:
        if tipo.upper() == "ALQUILER":
            return ContratoAlquiler(texto, cliente)
        elif tipo.upper() == "NDA":
            return ContratoNDA(texto, cliente)
        else:
            raise ValueError(f"Tipo de contrato no soportado: {tipo}")
