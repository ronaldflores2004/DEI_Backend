from app.analysis.providers.base_provider import (
    BaseAnalysisProvider
)


class OllamaProvider(
    BaseAnalysisProvider
):

    def analyze(
        self,
        text: str,
    ) -> dict:

        raise NotImplementedError(
            "Ollama aún no implementado."
        )