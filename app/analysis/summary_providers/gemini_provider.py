import logging

from google.genai import errors

from app.analysis.prompts import (
    build_summary_prompt
)

from app.analysis.summary_providers.base_provider import (
    BaseSummaryProvider
)

from app.shared.ai.gemini_client import (
    get_gemini_client
)

from app.shared.exceptions.ai_provider_exception import (
    AIProviderException
)


logger = logging.getLogger(__name__)


class GeminiSummaryProvider(
    BaseSummaryProvider
):
    """
    Proveedor de resúmenes semanales
    usando Gemini.
    """

    MODELS = (
        "gemini-2.5-flash",
        "gemini-2.5-flash-lite",
    )

    def generate(
        self,
        dominant_emotion: str,
        latest_emotion: str,
        risk_level: str,
        topics: list,
        triggers: list,
    ) -> str:

        prompt = build_summary_prompt(
            dominant_emotion,
            latest_emotion,
            risk_level,
            topics,
            triggers
        )

        last_error = None

        for model in self.MODELS:

            try:

                response = get_gemini_client().models.generate_content(
                    model=model,
                    contents=prompt
                )

                summary = (response.text or "").strip()

                if summary:
                    return summary

                last_error = AIProviderException(
                    f"{model} devolvió un resumen vacío."
                )

            except errors.APIError as e:

                last_error = e

            logger.warning(
                "%s falló generando el resumen semanal: %s",
                model,
                last_error
            )

        raise AIProviderException(
            "Gemini no pudo generar el resumen semanal."
        ) from last_error
