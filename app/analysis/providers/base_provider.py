from abc import ABC
from abc import abstractmethod


class BaseAnalysisProvider(ABC):
    """
    Contrato para cualquier proveedor
    de análisis emocional.
    """

    @abstractmethod
    def analyze(
        self,
        text: str,
    ) -> dict:
        pass