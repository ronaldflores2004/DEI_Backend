import json

from google import genai

from app.core.config import (
    GEMINI_API_KEY
)

from app.analysis.providers.base_provider import (
    BaseAnalysisProvider
)

from app.shared.enums.risk_level_enum import (
    RiskLevelEnum
)

from app.shared.enums.emotion_intensity_enum import (
    EmotionIntensityEnum
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

class GeminiProvider(
    BaseAnalysisProvider
):
    """
    Proveedor de análisis emocional
    utilizando Gemini.
    """

    @staticmethod
    def _call_model(
        text: str,
        model: str
    ) -> dict:

        prompt = f"""
        Eres un sistema de análisis emocional para una aplicación
        de apoyo terapéutico llamada DEI.

        Analiza el texto del paciente.

        Reglas obligatorias:

        - Responde solamente JSON válido.
        - No uses markdown.
        - No uses ```json.
        - Todo el contenido descriptivo debe estar en español.
        - Los valores de los enums deben escribirse EXACTAMENTE como se indican.
        - No traduzcas LOW, MEDIUM, HIGH ni CRITICAL.

        Usa únicamente estos niveles:

        emotion_intensity:
        LOW
        MEDIUM
        HIGH

        risk_level:
        LOW
        MEDIUM
        HIGH
        CRITICAL

        Formato exacto:

        {{
            "primary_emotion": "",
            "emotion_intensity": "",
            "risk_level": "",
            "analysis_json": {{
                "provider": "GEMINI",
                "model": "{model}",
                "sentiment": "",
                "topics": [],
                "triggers": []
            }}
        }}

        Texto del paciente:

        {text}
        """

        response = client.models.generate_content(
            model=model,
            contents=prompt
        )

        clean_response = (
            response.text
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        result = json.loads(
            clean_response
        )

        result["risk_level"] = RiskLevelEnum(
            result["risk_level"]
        )

        result["emotion_intensity"] = EmotionIntensityEnum(
            result["emotion_intensity"]
        )

        result["provider"] = "GEMINI"
        result["model"] = model

        result["analysis_json"]["provider"] = "GEMINI"
        result["analysis_json"]["model"] = model

        return result

    def analyze(
        self,
        text: str
    ) -> dict:

        try:

            return self._call_model(
                text=text,
                model="gemini-2.5-flash"
            )

        except errors.APIError as e:

            logger.warning(
                "Gemini Flash falló durante el análisis emocional: %s",
                e
            )

        try:

            return self._call_model(
                text=text,
                model="gemini-2.5-flash-lite"
            )

        except errors.APIError as e:

            logger.error(
                "Gemini Flash Lite también falló durante "
                "el análisis emocional: %s",
                e
            )

            raise AIProviderException(
                "Gemini no pudo realizar el análisis emocional."
            ) from e