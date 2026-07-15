from app.analysis.summary_providers.fake_provider import (
    FakeSummaryProvider
)

from app.analysis.summary_providers.gemini_provider import (
    GeminiSummaryProvider
)

from app.analysis.summary_providers.ollama_provider import (
    OllamaSummaryProvider
)


class SummaryProviderFactory:
    """
    Fábrica de proveedores para
    resúmenes semanales.
    """

    @staticmethod
    def get_provider(
        provider: str,
    ):

        provider = provider.upper()

        if provider == "GEMINI":
            return GeminiSummaryProvider()

        if provider == "FAKE":
            return FakeSummaryProvider()

        if provider == "OLLAMA":
            return OllamaSummaryProvider()

        raise ValueError(
            f"Proveedor '{provider}' no soportado."
        )