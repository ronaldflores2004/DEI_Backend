from app.analysis.models.emotional_analysis import (
    EmotionalAnalysis
)

from app.recommendations.providers.base_provider import (
    BaseRecommendationProvider
)


class FakeRecommendationProvider(
    BaseRecommendationProvider
):

    def generate(
        self,
        analysis: EmotionalAnalysis,
    ) -> dict:

        emotion = analysis.primary_emotion

        if emotion == "Ansiedad":
            return {
                "title": "Gestión de ansiedad",
                "content": (
                    "Has mostrado señales de ansiedad. "
                    "Intenta identificar las situaciones "
                    "que la desencadenan durante el día."
                ),
                "source": "FAKE"
            }

        if emotion == "Tristeza":
            return {
                "title": "Reflexión emocional",
                "content": (
                    "Dedica unos minutos a escribir "
                    "qué eventos han influido en tu estado emocional."
                ),
                "source": "FAKE"
            }

        if emotion == "Estrés":
            return {
                "title": "Manejo del estrés",
                "content": (
                    "Considera realizar pausas breves "
                    "durante actividades exigentes."
                ),
                "source": "FAKE"
            }

        return {
            "title": "Bienestar emocional",
            "content": (
                "Continúa registrando tus emociones "
                "para identificar patrones personales."
            ),
            "source": "FAKE"
        }