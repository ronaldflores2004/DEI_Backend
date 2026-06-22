import json

from google import genai

from app.core.config import (
    GEMINI_API_KEY
)


client = genai.Client(
    api_key=GEMINI_API_KEY
)


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
    - Todo debe estar en español.

    Usa únicamente estos niveles:

    emotion_intensity:
    Baja
    Media
    Alta

    risk_level:
    Bajo
    Medio
    Alto
    Crítico

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

    result["analysis_json"]["model"] = model

    return result


def analyze_text_with_gemini(
    text: str
):

    try:

        return call_model(
            text,
            "gemini-2.5-flash"
        )

    except Exception:

        return call_model(
            text,
            "gemini-2.5-flash-lite"
        )