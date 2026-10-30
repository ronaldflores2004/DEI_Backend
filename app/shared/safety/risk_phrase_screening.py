import re
import unicodedata

from app.shared.enums.risk_level_enum import (
    RiskLevelEnum
)


# =====================================
# FRASES DE RIESGO
# =====================================
#
# Filtro determinista que no depende de la IA.
# Las frases se escriben en minúsculas y sin tildes
# porque el texto se normaliza antes de compararlo.
#
# CRITICAL: intención o plan explícito.
# HIGH: ideación suicida o autolesión.
#
# Se prefiere alertar de más: una mención de
# suicidio sin ideación (por ejemplo, una película)
# también se marca HIGH para que el profesional
# la revise.

CRITICAL_PATTERNS = [
    r"\bme voy a (matar|suicidar)\b",
    r"\bvoy a (matarme|suicidarme|quitarme la vida)\b",
    r"\b(hoy|esta noche|manana) (me mato|me suicido|lo hago)\b",
    r"\btengo (un|el) plan para (matarme|suicidarme|morir)\b",
    r"\bya (compre|tengo) (las pastillas|la cuerda|el arma)\b",
    r"\bnota de despedida\b",
    r"\bcarta de despedida\b",
]

HIGH_PATTERNS = [
    r"\bsuicid\w*\b",
    r"\bquiero (morir|morirme|matarme)\b",
    r"\bganas de (morir|morirme|matarme)\b",
    r"\bno quiero (vivir|seguir viviendo|despertar)\b",
    r"\b(estaria|estarian) mejor (muerto|muerta|sin mi)\b",
    r"\bmejor (muerto|muerta)\b",
    r"\bquitarme la vida\b",
    r"\b(acabar|terminar) con (todo|mi vida)\b",
    r"\bhacerme dano\b",
    r"\b(me corto|cortarme|me corte|me hice cortes en) "
    r"(las |los |la |el )?(venas|brazos?|munecas?|piernas?)\b",
    r"\bautolesi\w*\b",
    r"\bdesaparecer para siempre\b",
    r"\bno vale la pena vivir\b",
]


def _normalize(
    text: str
) -> str:

    text = unicodedata.normalize(
        "NFKD",
        text.lower()
    )

    text = "".join(
        char
        for char in text
        if not unicodedata.combining(char)
    )

    return re.sub(r"\s+", " ", text)


def screen_risk_phrases(
    text: str | None
) -> RiskLevelEnum | None:
    """
    Devuelve CRITICAL o HIGH si el texto contiene
    frases de riesgo, o None si no encuentra ninguna.

    None no significa "sin riesgo": solo indica
    que este filtro no detectó frases conocidas.
    """

    if not text:
        return None

    normalized = _normalize(text)

    if any(
        re.search(pattern, normalized)
        for pattern in CRITICAL_PATTERNS
    ):
        return RiskLevelEnum.CRITICAL

    if any(
        re.search(pattern, normalized)
        for pattern in HIGH_PATTERNS
    ):
        return RiskLevelEnum.HIGH

    return None


RISK_ORDER = [
    RiskLevelEnum.LOW,
    RiskLevelEnum.MEDIUM,
    RiskLevelEnum.HIGH,
    RiskLevelEnum.CRITICAL,
]


def highest_risk(
    *levels: RiskLevelEnum | str | None
) -> RiskLevelEnum | None:
    """
    El nivel más alto entre los dados. Se usa para
    que el filtro de frases nunca quede por debajo
    de lo que dice la IA, ni la IA por debajo del
    filtro.
    """

    valid = [
        RiskLevelEnum(level)
        for level in levels
        if level in [risk.value for risk in RISK_ORDER]
    ]

    if not valid:
        return None

    return max(valid, key=RISK_ORDER.index)
