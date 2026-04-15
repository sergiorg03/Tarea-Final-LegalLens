from abc import ABC, abstractmethod

class Contrato(ABC):
    def __init__(self, texto):
        self.texto = texto

    @abstractmethod
    def analizar(self):
        pass


class ContratoAlquiler(Contrato):
    def analizar(self):
        return "Analizando alquiler"


class ContratoConfidencialidad(Contrato):
    def analizar(self):
        return "Analizando NDA"