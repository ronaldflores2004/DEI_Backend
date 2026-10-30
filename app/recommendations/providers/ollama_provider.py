from app.analysis.models.emotional_analysis import (
    EmotionalAnalysis
)

from app.recommendations.prompts import (
    build_recommendation_prompt
)

from app.recommendations.providers.base_provider import (
    BaseRecommendationProvider
)

from app.shared.ai.ollama_client import (
    OllamaClient
)

from app.shared.exceptions.ai_provider_exception import (
    AIProviderException
)


class OllamaRecommendationProvider(
    BaseRecommendationProvider
):
    """
    Proveedor de recomendaciones
    usando la IA local (Ollama).
    """

    def generate(
        self,
        analysis: EmotionalAnalysis,
    ) -> dict:

        data = OllamaClient.generate_json(
            build_recommendation_prompt(analysis)
        )

        title = str(data.get("title") or "").strip()
        content = str(data.get("content") or "").strip()

        if not title or not content:
            raise AIProviderException(
                "Ollama devolvió una recomendación incompleta."
            )

        return {
            "title": title[:255],
            "content": content,
            "source": "OLLAMA"
        }
