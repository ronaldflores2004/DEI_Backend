def analyze_text(text: str):

    text_lower = text.lower()

    primary_emotion = "Calma"
    emotion_intensity = "Baja"
    risk_level = "Bajo"

    if "triste" in text_lower:
        primary_emotion = "Tristeza"
        emotion_intensity = "Media"

    if "ansiedad" in text_lower:
        primary_emotion = "Ansiedad"
        emotion_intensity = "Alta"

    if "miedo" in text_lower:
        primary_emotion = "Miedo"

    if "estres" in text_lower:
        primary_emotion = "Estrés"

    return {
        "primary_emotion": primary_emotion,
        "emotion_intensity": emotion_intensity,
        "risk_level": risk_level,
        "analysis_json": {
            "provider": "FAKE_ANALYSIS",
            "text_length": len(text),
            "keywords_detected": [
                word
                for word in [
                    "triste",
                    "ansiedad",
                    "miedo",
                    "estres"
                ]
                if word in text_lower
            ]
        }
    }