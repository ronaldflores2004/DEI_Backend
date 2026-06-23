from google import genai

from app.core.config import (
    GEMINI_API_KEY
)

client = genai.Client(
    api_key=GEMINI_API_KEY
)


def generate_ai_summary(
    dominant_emotion: str,
    latest_emotion: str,
    risk_level: str,
    topics: list,
    triggers: list
):

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

    except Exception:

        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt
        )

        return response.text.strip()