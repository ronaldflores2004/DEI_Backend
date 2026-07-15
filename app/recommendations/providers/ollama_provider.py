from app.analysis.models.emotional_analysis import (
    EmotionalAnalysis
)

from app.recommendations.providers.base_provider import (
    BaseRecommendationProvider
)


class OllamaRecommendationProvider(
    BaseRecommendationProvider
):

    def generate(
        self,
        analysis: EmotionalAnalysis,
    ) -> dict:

        raise NotImplementedError(
            "Ollama Recommendation Provider aún no implementado."
        )