"""
Prompts compartidos por todos los proveedores
de IA (Gemini, Ollama, ...).

Mantenerlos en un solo lugar garantiza que la IA
local y Gemini reciban exactamente las mismas
instrucciones y devuelvan el mismo formato.
"""


def build_analysis_prompt(
    text: str,
) -> str:

    return f"""
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
        "sentiment": "",
        "topics": [],
        "triggers": []
    }}
}}

Texto del paciente:

{text}
"""


def build_summary_prompt(
    dominant_emotion: str,
    latest_emotion: str,
    risk_level: str,
    topics: list,
    triggers: list,
) -> str:

    return f"""
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
- Responde solo con el resumen, sin títulos ni comillas.
"""
