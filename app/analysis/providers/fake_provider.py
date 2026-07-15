from app.analysis.services.fake_analysis_service import (
    analyze_text_with_fake
)

from app.analysis.providers.base_provider import (
    BaseAnalysisProvider
)


class FakeProvider(
    BaseAnalysisProvider
):

    def analyze(
        self,
        text: str,
    ) -> dict:

        return analyze_text_with_fake(text)