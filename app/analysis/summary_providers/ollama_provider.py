from app.analysis.summary_providers.base_provider import (
    BaseSummaryProvider
)


class OllamaSummaryProvider(
    BaseSummaryProvider
):

    def generate(
        self,
        dominant_emotion: str,
        latest_emotion: str,
        risk_level: str,
        topics: list,
        triggers: list,
    ) -> str:

        raise NotImplementedError(
            "Ollama Summary Provider aún no implementado."
        )