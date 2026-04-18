from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import List

# Definicion de los datos que extraermos del PDF
class EntidadesExtraidas(BaseModel):
    nombres: List[str]
    dni: List[str]
    fechas: List[str]
    importes: List[str]

# Molde final para la respuesta de la IA
class AnalisisResultado(BaseModel):
    puntos_clave: List[str]
    banderas_rojas: List[str]
    riesgo_total: str  # "Bajo", "Medio" o "Critico"
    entidades: EntidadesExtraidas

# Clase base abstracta usando patron Template Method
class Contrato(ABC):
    def __init__(self, texto: str, cliente: str):
        self.texto = texto
        self.cliente = cliente

    @abstractmethod
    def obtener_prompt_especifico(self) -> str:
        # Cada tipo de contrato definira sus propios criterios
        pass

    def ejecutar_auditoria(self, agente_ia) -> dict:
        """
        Método Plantilla (Template Method): Define el flujo de la auditoría.
        Es común para todos los contratos, pero usa prompts específicos de los hijos.
        """
        prompt = self.obtener_prompt_especifico()
        return agente_ia.analizar(self.texto, prompt)

# Implementacion para alquileres
class ContratoAlquiler(Contrato):
    def obtener_prompt_especifico(self) -> str:
        return """
        Busca especificamente:
        1. Si la fianza exigida supera el limite legal (1 mes).
        2. Si el contrato obliga al inquilino a pagar reparaciones estructurales (Art. 21 LAU).
        3. Clausulas de acceso del casero a la vivienda sin aviso.
        """

# Implementacion para NDA
class ContratoNDA(Contrato):
    def obtener_prompt_especifico(self) -> str:
        return """
        Busca especificamente:
        1. Clausulas de duracion infinita o perpetua.
        2. Multas desproporcionadas (superiores a 100.000E).
        3. Definiciones de informacion confidencial demasiado amplias.
        """

# Fabrica para crear el objeto contrato segun el tipo
class ContratoFactory:
    @staticmethod
    def crear_contrato(tipo: str, texto: str, cliente: str) -> Contrato:
        if tipo.upper() == "ALQUILER":
            return ContratoAlquiler(texto, cliente)
        elif tipo.upper() == "NDA":
            return ContratoNDA(texto, cliente)
        else:
            raise ValueError(f"Tipo de contrato desconocido: {tipo}")
        
