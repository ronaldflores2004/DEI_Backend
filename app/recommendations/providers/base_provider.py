from abc import ABC
from abc import abstractmethod

from app.analysis.models.emotional_analysis import (
    EmotionalAnalysis
)


class BaseRecommendationProvider(ABC):
    """
    Interfaz para los proveedores de
    recomendaciones.
    """

    @abstractmethod
    def generate(
        self,
        analysis: EmotionalAnalysis,
    ) -> dict:
        pass