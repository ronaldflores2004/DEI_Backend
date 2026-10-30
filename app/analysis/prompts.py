"""
Prompts compartidos por todos los proveedores
de IA (Gemini, Ollama, ...).

Mantenerlos en un solo lugar garantiza que la IA
local y Gemini reciban exactamente las mismas
instrucciones y devuelvan el mismo formato.
"""

from app.shared.emotions import EMOTIONS


def build_analysis_prompt(
    text: str,
) -> str:

    emotions = "\n".join(EMOTIONS)

    return f"""
Eres un asistente de registro emocional para DEI, una
aplicación de apoyo a la terapia psicológica. Describes
lo que el paciente expresa; no diagnosticas ni
recomiendas tratamientos. La evaluación clínica la hace
siempre el profesional.

Analiza el texto del paciente.

Reglas obligatorias:

- Responde solamente JSON válido.
- No uses markdown.
- No uses ```json.
- Todo el contenido descriptivo debe estar en español.
- Los valores de los enums deben escribirse EXACTAMENTE como se indican.
- No traduzcas LOW, MEDIUM, HIGH ni CRITICAL.
- No inventes: usa solo lo que dice el texto. Si el texto
  es muy breve o ambiguo, elige la opción más baja que
  sea coherente con lo escrito.
- No uses términos diagnósticos (por ejemplo "depresión
  mayor" o "trastorno").

primary_emotion: una sola de esta lista, escrita igual:
{emotions}

emotion_intensity:
LOW: la emoción se menciona de paso o es leve.
MEDIUM: la emoción es clara y afecta el día del paciente.
HIGH: la emoción es intensa, desbordante o domina el texto.

risk_level (riesgo para la vida o integridad del
paciente o de otras personas):
LOW: sin señales de riesgo.
MEDIUM: malestar intenso, desesperanza, aislamiento o
consumo problemático, sin ideas de hacerse daño.
HIGH: ideas de muerte o suicidio, deseo de no vivir,
autolesiones, o sufrir violencia o abuso.
CRITICAL: intención o plan de suicidio o de hacer daño,
acceso a medios (pastillas, armas), despedidas, o
peligro inmediato.
Ante la duda entre dos niveles de riesgo, elige el más alto.

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
