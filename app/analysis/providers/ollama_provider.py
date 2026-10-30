from app.core.config import (
    settings
)

from app.analysis.prompts import (
    build_analysis_prompt
)

from app.analysis.providers.analysis_parser import (
    AnalysisParser
)

from app.analysis.providers.base_provider import (
    BaseAnalysisProvider
)

from app.shared.ai.ollama_client import (
    OllamaClient
)


class OllamaProvider(
    BaseAnalysisProvider
):
    """
    Proveedor de análisis emocional
    utilizando la IA local (Ollama).
    """

    def analyze(
        self,
        text: str,
    ) -> dict:

        data = OllamaClient.generate_json(
            build_analysis_prompt(text)
        )

        return AnalysisParser.from_dict(
            data=data,
            provider="OLLAMA",
            model=settings.OLLAMA_MODEL
        )
