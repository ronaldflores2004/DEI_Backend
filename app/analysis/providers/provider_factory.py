from app.analysis.providers.gemini_provider import (
    GeminiProvider
)

from app.analysis.providers.fake_provider import (
    FakeProvider
)

from app.analysis.providers.ollama_provider import (
    OllamaProvider
)
from app.analysis.providers.base_provider import (
    BaseAnalysisProvider
)


class AnalysisProviderFactory:
    """
    Fábrica encargada de devolver
    el proveedor de IA correspondiente.
    """

    @staticmethod
    def get_provider(
        provider: str,
    ) -> BaseAnalysisProvider:

        provider = provider.upper()

        if provider == "GEMINI":
            return GeminiProvider()

        elif provider == "FAKE":
            return FakeProvider()

        elif provider == "OLLAMA":
            return OllamaProvider()

        raise ValueError(
            f"Proveedor '{provider}' no soportado."
        )