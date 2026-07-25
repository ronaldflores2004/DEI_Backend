from google import genai

from app.core.config import (
    GEMINI_API_KEY
)

from app.analysis.summary_providers.base_provider import (
    BaseSummaryProvider
)

import logging

from google.genai import errors

from app.shared.exceptions.ai_provider_exception import (
    AIProviderException
)


client = genai.Client(
    api_key=GEMINI_API_KEY
)

logger = logging.getLogger(__name__)

class GeminiSummaryProvider(
    BaseSummaryProvider
):
    """
    Proveedor de resúmenes semanales
    usando Gemini.
    """

    def generate(
        self,
        dominant_emotion: str,
        latest_emotion: str,
        risk_level: str,
        topics: list,
        triggers: list,
    ) -> str:

        prompt = f"""
Genera un resumen breve para un paciente.

Emoción predominante:
{dominant_emotion}

Última emoción:
{latest_emotion}

Nivel de riesgo:
{risk_level}

Temas identificados:
{topics}

Desencadenantes identificados:
{triggers}

Reglas:
- Lenguaje sencillo.
- Español.
- Máximo 2 oraciones.
- No hagas diagnósticos.
"""

        try:

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            return response.text.strip()

        except errors.APIError as e:

            logger.warning(
                "Gemini Flash falló generando el resumen semanal: %s",
                e
            )

        try:

            response = client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=prompt
            )

            return response.text.strip()

        except errors.APIError as e:

            logger.error(
                "Gemini Flash Lite también falló generando "
                "el resumen semanal: %s",
                e
            )

            raise AIProviderException(
                "Gemini no pudo generar el resumen semanal."
            ) from e