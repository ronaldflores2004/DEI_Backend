from app.analysis.services.gemini_analysis_service import (
    GeminiAnalysisService
)

from app.analysis.providers.base_provider import (
    BaseAnalysisProvider
)


class GeminiProvider(
    BaseAnalysisProvider
):

    def analyze(
        self,
        text: str,
    ) -> dict:

        return (
            GeminiAnalysisService
            .analyze_text_with_gemini(text)
        )