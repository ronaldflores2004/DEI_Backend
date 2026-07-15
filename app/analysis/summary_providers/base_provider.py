from abc import ABC
from abc import abstractmethod


class BaseSummaryProvider(ABC):
    """
    Interfaz para los proveedores
    de resúmenes semanales.
    """

    @abstractmethod
    def generate(
        self,
        dominant_emotion: str,
        latest_emotion: str,
        risk_level: str,
        topics: list,
        triggers: list,
    ) -> str:
        pass