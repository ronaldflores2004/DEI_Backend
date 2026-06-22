from collections import Counter

from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.identity.models.patient_profile import (
    PatientProfile
)

from app.entries.models.emotional_entry import (
    EmotionalEntry
)

from app.analysis.models.emotional_analysis import (
    EmotionalAnalysis
)

from datetime import datetime, timedelta


def get_weekly_summary(
    current_user_id: int,
    db: Session
):

    patient = (
        db.query(PatientProfile)
        .filter(
            PatientProfile.user_id == current_user_id
        )
        .first()
    )

    if not patient:
        raise HTTPException(
            status_code=403,
            detail="No tienes perfil de paciente"
        )

    week_ago = (
        datetime.utcnow()
        - timedelta(days=7)
    )

    analyses = (
        db.query(EmotionalAnalysis)
        .join(
            EmotionalEntry,
            EmotionalAnalysis.entry_id == EmotionalEntry.id
        )
        .filter(
            EmotionalEntry.patient_id == patient.id
        )
        .filter(
            EmotionalAnalysis.analyzed_at >= week_ago
        )
        .all()
    )
    
    if not analyses:
        return {
            "entries_count": 0,
            "dominant_emotion": None,
            "latest_emotion": None,
            "average_intensity": None,
            "risk_level": None,
            "trend": "SIN_DATOS",
            "recommendation": (
                "Todavía no existen análisis emocionales."
            )
        }

    emotions = [
        analysis.primary_emotion
        for analysis in analyses
        if analysis.primary_emotion
    ]

    dominant_emotion = (
        Counter(emotions)
        .most_common(1)[0][0]
    )

    risks = [
        analysis.risk_level
        for analysis in analyses
        if analysis.risk_level
    ]

    risk_level = (
        Counter(risks)
        .most_common(1)[0][0]
    )
    
    intensities = [
        analysis.emotion_intensity
        for analysis in analyses
        if analysis.emotion_intensity
    ]

    average_intensity = None

    if intensities:

        intensity_values = {
            "Baja": 1,
            "Media": 2,
            "Alta": 3
        }

        reverse_values = {
            1: "Baja",
            2: "Media",
            3: "Alta"
        }

        valid_intensities = [
            i
            for i in intensities
            if i in intensity_values
        ]


        if valid_intensities:

            total = sum(
                intensity_values[i]
                for i in valid_intensities
            )

            average = (
                total /
                len(valid_intensities)
            )

        else:

            average = 1


        average = round(
            total / len(intensities)
        )

        average_intensity = (
            reverse_values[average]
        )

    latest_analysis = sorted(
        analyses,
        key=lambda x: x.analyzed_at,
        reverse=True
    )[0]

    latest_emotion = (
        latest_analysis.primary_emotion
    )

    trend = "ESTABLE"

    if latest_emotion in [
        "Ansiedad",
        "Tristeza",
        "Miedo",
        "Estrés"
    ]:
        trend = "ATENCION"

    if latest_emotion == "Calma":
        trend = "MEJORA"

    return {
        "entries_count": len(analyses),
        "dominant_emotion": dominant_emotion,
        "latest_emotion": latest_emotion,
        "risk_level": risk_level,
        "trend": trend,
        "average_intensity": average_intensity,
        "recommendation":
            f"Tu emoción predominante fue {dominant_emotion}. Continúa registrando tus emociones para identificar patrones."
    }
    