import json

from app.shared.enums.risk_level_enum import (
    RiskLevelEnum
)

from app.shared.enums.emotion_intensity_enum import (
    EmotionIntensityEnum
)

from app.shared.emotions import (
    normalize_emotion
)

from app.shared.exceptions.ai_provider_exception import (
    AIProviderException
)


class AnalysisParser:
    """
    Valida y normaliza la respuesta de un modelo
    para el análisis emocional.

    Si la respuesta no cumple el formato, lanza
    AIProviderException para activar el respaldo.
    """

    @staticmethod
    def from_text(
        raw: str,
        provider: str,
        model: str,
    ) -> dict:

        clean = (
            (raw or "")
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        try:

            data = json.loads(clean)

        except json.JSONDecodeError as e:

            raise AIProviderException(
                f"{provider} devolvió JSON inválido."
            ) from e

        return AnalysisParser.from_dict(
            data=data,
            provider=provider,
            model=model
        )

    @staticmethod
    def from_dict(
        data: dict,
        provider: str,
        model: str,
    ) -> dict:

        try:

            primary_emotion = normalize_emotion(
                str(data["primary_emotion"])
            )

            emotion_intensity = EmotionIntensityEnum(
                str(data["emotion_intensity"]).strip().upper()
            )

            risk_level = RiskLevelEnum(
                str(data["risk_level"]).strip().upper()
            )

            analysis_json = data.get("analysis_json") or {}

            if not isinstance(analysis_json, dict):
                raise TypeError("analysis_json debe ser un objeto")

        except (
            KeyError,
            TypeError,
            ValueError,
        ) as e:

            raise AIProviderException(
                f"{provider} devolvió un análisis incompleto: {e}"
            ) from e

        if not primary_emotion:
            raise AIProviderException(
                f"{provider} no indicó la emoción principal."
            )

        analysis_json.setdefault("sentiment", "")
        analysis_json.setdefault("topics", [])
        analysis_json.setdefault("triggers", [])

        analysis_json["provider"] = provider
        analysis_json["model"] = model

        return {
            "primary_emotion": primary_emotion,
            "emotion_intensity": emotion_intensity,
            "risk_level": risk_level,
            "provider": provider,
            "model": model,
            "analysis_json": analysis_json
        }
