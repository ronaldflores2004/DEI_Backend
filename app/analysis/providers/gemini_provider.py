import logging

from google.genai import errors

from app.analysis.prompts import (
    build_analysis_prompt
)

from app.analysis.providers.analysis_parser import (
    AnalysisParser
)

from app.analysis.providers.base_provider import (
    BaseAnalysisProvider
)

from app.shared.ai.gemini_client import (
    get_gemini_client
)

from app.shared.exceptions.ai_provider_exception import (
    AIProviderException
)


logger = logging.getLogger(__name__)


class GeminiProvider(
    BaseAnalysisProvider
):
    """
    Proveedor de análisis emocional
    utilizando Gemini.
    """

    MODELS = (
        "gemini-2.5-flash",
        "gemini-2.5-flash-lite",
    )

    @staticmethod
    def _call_model(
        text: str,
        model: str
    ) -> dict:

        try:

            response = get_gemini_client().models.generate_content(
                model=model,
                contents=build_analysis_prompt(text)
            )

        except errors.APIError as e:

            raise AIProviderException(
                f"{model} falló: {e}"
            ) from e

        return AnalysisParser.from_text(
            raw=response.text,
            provider="GEMINI",
            model=model
        )

    def analyze(
        self,
        text: str
    ) -> dict:

        last_error = None

        for model in self.MODELS:

            try:

                return self._call_model(
                    text=text,
                    model=model
                )

            except AIProviderException as e:

                logger.warning(
                    "Gemini falló durante el análisis emocional: %s",
                    e
                )

                last_error = e

        raise AIProviderException(
            "Gemini no pudo realizar el análisis emocional."
        ) from last_error
