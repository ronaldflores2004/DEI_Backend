import json

from google import genai

from app.core.config import (
    GEMINI_API_KEY
)

from app.shared.enums.risk_level_enum import RiskLevelEnum
from app.shared.enums.emotion_intensity_enum import EmotionIntensityEnum


client = genai.Client(
    api_key=GEMINI_API_KEY
)

class GeminiAnalysisService:
    """Servicio para análisis emocional usando Gemini."""
    
    @staticmethod
    def call_model(
        text: str,
        model: str
    ):

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

        result = json.loads(clean_response)
        
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

    @staticmethod
    def analyze_text_with_gemini(
        text: str
    ):

        try:

            return GeminiAnalysisService.call_model(
                text,
                "gemini-2.5-flash"
            )

        except Exception:

            return GeminiAnalysisService.call_model(
                text,
                "gemini-2.5-flash-lite"
            )