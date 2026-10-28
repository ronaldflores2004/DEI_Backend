from app.analysis.prompts import (
    build_summary_prompt
)

from app.analysis.summary_providers.base_provider import (
    BaseSummaryProvider
)

from app.shared.ai.ollama_client import (
    OllamaClient
)


class OllamaSummaryProvider(
    BaseSummaryProvider
):
    """
    Proveedor de resúmenes semanales
    usando la IA local (Ollama).
    """

    def generate(
        self,
        dominant_emotion: str,
        latest_emotion: str,
        risk_level: str,
        topics: list,
        triggers: list,
    ) -> str:

        return OllamaClient.generate(
            build_summary_prompt(
                dominant_emotion,
                latest_emotion,
                risk_level,
                topics,
                triggers
            )
        ).strip('"')
