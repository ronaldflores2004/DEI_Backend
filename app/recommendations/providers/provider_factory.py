from app.recommendations.providers.fake_provider import (
    FakeRecommendationProvider
)

from app.recommendations.providers.gemini_provider import (
    GeminiRecommendationProvider
)

from app.recommendations.providers.ollama_provider import (
    OllamaRecommendationProvider
)


class RecommendationProviderFactory:
    """
    Fábrica encargada de devolver
    el proveedor de recomendaciones.
    """

    @staticmethod
    def get_provider(
        provider: str,
    ):

        provider = provider.upper()

        if provider == "FAKE":
            return FakeRecommendationProvider()

        if provider == "GEMINI":
            return GeminiRecommendationProvider()

        if provider == "OLLAMA":
            return OllamaRecommendationProvider()

        raise ValueError(
            f"Proveedor '{provider}' no soportado."
        )