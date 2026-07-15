from app.analysis.models.emotional_analysis import (
    EmotionalAnalysis
)

from app.recommendations.providers.base_provider import (
    BaseRecommendationProvider
)


class GeminiRecommendationProvider(
    BaseRecommendationProvider
):

    def generate(
        self,
        analysis: EmotionalAnalysis,
    ) -> dict:

        raise NotImplementedError(
            "Gemini Recommendation Provider aún no implementado."
        )