import unicodedata


# =====================================
# CATÁLOGO DE EMOCIONES
# =====================================
#
# Nombre canónico (el que se guarda y se muestra).
# La IA local, Gemini y DEI_AI pueden devolver
# variantes ("TRISTEZA", "tristeza", "Estres"):
# normalize_emotion las lleva a este nombre.

EMOTIONS = [
    "Alegría",
    "Tristeza",
    "Ansiedad",
    "Miedo",
    "Ira",
    "Asco",
    "Sorpresa",
    "Calma",
    "Estrés",
    "Desánimo",
    "Culpa",
    "Vergüenza",
    "Soledad",
    "Frustración",
    "Confusión",
    "Esperanza",
    "Confianza",
    "Gratitud",
    "Agotamiento",
    "Amor",
    "Preocupación",
    "Desesperanza",
]

NEGATIVE_EMOTIONS = {
    "Tristeza",
    "Ansiedad",
    "Miedo",
    "Ira",
    "Estrés",
    "Desánimo",
    "Culpa",
    "Vergüenza",
    "Soledad",
    "Frustración",
    "Agotamiento",
    "Preocupación",
    "Desesperanza",
}

POSITIVE_EMOTIONS = {
    "Alegría",
    "Calma",
    "Esperanza",
    "Confianza",
    "Gratitud",
    "Amor",
}


def _key(
    emotion: str
) -> str:

    emotion = unicodedata.normalize(
        "NFKD",
        emotion.strip().lower()
    )

    return "".join(
        char
        for char in emotion
        if not unicodedata.combining(char)
    )


_CANONICAL = {
    _key(emotion): emotion
    for emotion in EMOTIONS
}


def normalize_emotion(
    emotion: str | None
) -> str | None:
    """
    Devuelve el nombre canónico. Si la emoción no
    está en el catálogo se conserva, capitalizada.
    """

    if not emotion or not emotion.strip():
        return None

    return _CANONICAL.get(
        _key(emotion),
        emotion.strip().capitalize()
    )


def is_negative(
    emotion: str | None
) -> bool:

    return normalize_emotion(emotion) in NEGATIVE_EMOTIONS


def is_positive(
    emotion: str | None
) -> bool:

    return normalize_emotion(emotion) in POSITIVE_EMOTIONS
