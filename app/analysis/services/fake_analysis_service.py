from app.shared.enums.risk_level_enum import (
    RiskLevelEnum
)

from app.shared.enums.emotion_intensity_enum import (
    EmotionIntensityEnum
)

def analyze_text_with_fake(text: str):

    text_lower = text.lower()

    primary_emotion = "Calma"
    emotion_intensity = EmotionIntensityEnum.LOW
    risk_level = RiskLevelEnum.LOW

    keywords_detected = []

    topics = []

    triggers = []

    sentiment = "Neutral"

    # Emociones

    if "triste" in text_lower:

        primary_emotion = "Tristeza"

        emotion_intensity = EmotionIntensityEnum.MEDIUM

        sentiment = "Negativo"

        keywords_detected.append("triste")

    if "ansiedad" in text_lower:

        primary_emotion = "Ansiedad"

        emotion_intensity = EmotionIntensityEnum.HIGH

        risk_level = RiskLevelEnum.MEDIUM

        sentiment = "Negativo"

        keywords_detected.append("ansiedad")

    if "miedo" in text_lower:

        primary_emotion = "Miedo"

        emotion_intensity = EmotionIntensityEnum.HIGH

        risk_level = RiskLevelEnum.HIGH

        sentiment = "Negativo"

        keywords_detected.append("miedo")

    if "estres" in text_lower:

        primary_emotion = "Estrés"

        emotion_intensity = EmotionIntensityEnum.HIGH

        risk_level = RiskLevelEnum.MEDIUM

        sentiment = "Negativo"

        keywords_detected.append("estres")

    # Temas

    if "trabajo" in text_lower:

        topics.append("Trabajo")

        triggers.append("Presión laboral")

    if "familia" in text_lower:

        topics.append("Familia")

        triggers.append("Conflictos familiares")

    if "universidad" in text_lower:

        topics.append("Estudios")

        triggers.append("Exigencia académica")

    if "pareja" in text_lower:

        topics.append("Relaciones")

        triggers.append("Conflictos de pareja")

    return {
        "provider": "FAKE_ANALYSIS",
        "model": "RULE_ENGINE_V1",

        "primary_emotion": primary_emotion,

        "emotion_intensity": emotion_intensity,

        "risk_level": risk_level,

        "analysis_json": {

            "provider": "FAKE_ANALYSIS",

            "model": "RULE_ENGINE_V1",

            "text_length": len(text),

            "sentiment": sentiment,

            "keywords_detected": keywords_detected,

            "topics": topics,

            "triggers": triggers
        }
    }