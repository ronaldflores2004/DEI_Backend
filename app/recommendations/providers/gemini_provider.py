from app.analysis.models.emotional_analysis import (
    EmotionalAnalysis
)

from app.recommendations.providers.base_provider import (
    BaseRecommendationProvider
)

from app.shared.exceptions.ai_provider_exception import (
    AIProviderException
)


class GeminiRecommendationProvider(
    BaseRecommendationProvider
):

    def generate(
        self,
        analysis: EmotionalAnalysis,
    ) -> dict:

        raise AIProviderException(
            "Gemini Recommendation Provider aún no implementado."
        )