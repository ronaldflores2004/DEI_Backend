from app.analysis.models.emotional_analysis import (
    EmotionalAnalysis
)


def build_recommendation_prompt(
    analysis: EmotionalAnalysis,
) -> str:

    data = analysis.analysis_json or {}

    return f"""
Eres un asistente de bienestar emocional de la aplicación DEI.

Genera UNA recomendación breve y práctica para el paciente
a partir de este análisis emocional.

Emoción principal:
{analysis.primary_emotion}

Intensidad:
{analysis.emotion_intensity}

Nivel de riesgo:
{analysis.risk_level}

Temas:
{data.get("topics", [])}

Desencadenantes:
{data.get("triggers", [])}

Reglas obligatorias:

- Responde solamente JSON válido.
- Español, lenguaje sencillo y cercano.
- "title": máximo 60 caracteres.
- "content": máximo 3 oraciones.
- No hagas diagnósticos ni recomiendes medicamentos.
- Si el riesgo es HIGH o CRITICAL, sugiere contactar a su
  profesional o a una línea de ayuda.

Formato exacto:

{{
    "title": "",
    "content": ""
}}
"""
